import psycopg2
import sys, re
#from imp import reload

#reload(sys)


# 根据医生得分排序
def by_score(t):
    return -t[1]

def list(area,disease):
    # 数据库连接参数
    conn = psycopg2.connect(database="postgres", user="postgres", password="root", host="127.0.0.1", port="5432")
    # conn.set_client_encoding('utf-8')
    cur = conn.cursor()

    # 根据地区和擅长疾病推荐
    def get_doctor(area, disease):
        nonlocal cur
        # ---得到帮助患者列的最大值---#
        cur.execute(
            "SELECT max(help_patients_num ::Integer) FROM public.doctor_info where area='" + area + "' and work_on like '%" + disease + "%'")
        max_num = cur.fetchall()[0][0]

        # ---根据地区和擅长疾病查询符合条件医生---#
        cur.execute(
            "SELECT doctor_id,help_patients_num,patient_votes,hos_level FROM public.doctor_info,public.hospital where area='" + area + "' and work_on like '%" + disease + "%' and public.doctor_info.hospital =public.hospital.hos_name")
        rows = cur.fetchall()

        # ---对于患者投票列中，得到各个医生对查询疾病的投票比例以及该比例的最大值---#
        temp_list = []
        level_list = []
        for tup in rows:
            votes = tup[2]  # 患者对该医生投票
            disease_vote = 0  # 患者针对目前查询疾病的投票，默认为0
            hos_level = tup[3]
            if votes != '近两年暂无患者投票' and disease in votes:
                # 全部票数
                num_list = re.findall(r'\d+', votes)
                vote_sum = sum(int(i) for i in num_list)
                # 该疾病投票
                index = votes.index(disease)
                votes = votes[index:]
                index_1 = votes.index('(')
                index_2 = votes.index('票')
                disease_vote = int(votes[index_1 + 1:index_2])
                # 查询疾病投票在总投票中的比例
                proportion = disease_vote / vote_sum
                temp_list.append(proportion)
            else:
                temp_list.append(0)
        # 得到所有比例中的最大值
        max_proportion = max(temp_list)

        # ---为每个医生排序---#
        # 打分规则：(帮助患者次数/max_num )*0.4+(查询疾病投票比例/max_proportion)*0.6
        # 分别除以最大值的原因是，使这两个值都是<=1。
        # 不会因为帮助患者次数这个值太大，使得打分严重依赖于该列，以及消除若该疾病的投票比例很小，而该值远小于1的情况。
        num_weight = 0.4  # 帮助患者次数比重为40%，
        i = 0  # 用来bianlitemp_list
        doctor_list = []
        for tup in rows:
            doctor_id = tup[0]  # 医生编号
            help_patients_num = int(tup[1])  # 帮助患者次数
            # 该医生针对该查询疾病的综合打分:帮助患者次数比重为40%，该疾病投票为60%
            score = (help_patients_num / max_num) * num_weight + (temp_list[i] / max_proportion) * (1 - num_weight)
            i += 1
            doctor_tuple = (doctor_id, score)  # 医生和该医生针对该疾病的打分的映射
            doctor_list.append(doctor_tuple)
        # 以score对医生进行排序
        doctor_list = sorted(doctor_list, key=by_score)

        return doctor_list

    list = []
    doctors = get_doctor(area, disease)
    for doctor in doctors:
        cur.execute("SELECT * FROM public.doctor_info where doctor_id=" + str(doctor[0]))
        rows = cur.fetchall()

        for i in rows:
            list.append(i)

    conn.commit()
    cur.close()
    conn.close()
    return list


if __name__ == '__main__':
    a = list('北京', '糖尿病')
    print(a[11][14])

