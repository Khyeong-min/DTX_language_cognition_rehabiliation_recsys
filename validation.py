import random
import pandas as pd

# 0. pickle 파일 불러오기
final_df = pd.read_pickle("final_df_for_clustering_algorithm.pkl")

# 1. 랜덤하게 [*, *]로 packing하기(16명의 사람, 21개의 문제)
val_df = final_df.copy()
for i in random.sample(range(1, len(val_df.index)), 16):
    for j in random.sample(range(1, len(val_df.columns)), 21):
        val_df.loc[val_df.index[i], val_df.columns[j]] = ['*', '*']


# 2. 클러스터를 찾아주는 함수
def find_cluster(indexs_list):
    all_cluster = pd.read_pickle("patient_cluster_series.pkl")
    cluster_list = []
    index = 0
    #[[19, [14, 25, 33]]
    #-1이 있는 환자들이 속한 클러스터를 all_cluster를 돌면서 찾기-> cluster: -1이 있는 환자들이 속한 클러스터
    for index in range(len(indexs_list)):
        for cluster in all_cluster:
            if cluster != None:
                if indexs_list[index][0] in cluster:
                    cluster_list.append([indexs_list[index][0], indexs_list[index][1], cluster])
                    break
                else:
                    continue
            else:
                pass
    return cluster_list


# 4. 클러스터를 돌면서 값을 찾아서 average값으로 추출
def find_value_for_packing(indexs_list):
    # -1이 있는 곳에 클러스터가 가진 모든 값을 average를 내서 채워넣기
    # cluster_list[0] = -1 이 있는 사람/ cluster_list[1] = 그 사람에게 -1이 있는 문항/ cluster_list[2] = 사람이 있는 클러스터 집단
    cluster_list = find_cluster(indexs_list)
    error_list = []
    packing_lists = []
    for cluster_index in range(len(cluster_list)):  # 본인
        for problem_num in cluster_list[cluster_index][1]:  # 문제
            added_correct_value_from_clustering = 0
            added_response_value_from_clustering = 0
            count = 0
            packing_list = []
            for person_in_cluster_num in cluster_list[cluster_index][2]:  # 비슷한 사람
                # 평균 정/오답 확률
                if (val_df.iloc[person_in_cluster_num][problem_num][0] != '*') and (val_df.iloc[person_in_cluster_num][problem_num][1] != '*'):
                    correct_val = int(val_df.iloc[person_in_cluster_num][problem_num][0])
                    added_correct_value_from_clustering += correct_val
                    # 평균 소요 시간
                    response_val = int(val_df.iloc[person_in_cluster_num][problem_num][1])
                    added_response_value_from_clustering += response_val
                count += 1
            if count > 0:
                # 정/오답 확률 평균으로 계산
                correct_value = added_correct_value_from_clustering / count
                # 평균 소요 시간 확률 평균으로 계산
                response_value = added_response_value_from_clustering / count
                list_value = [correct_value, response_value]
                packing_list = [cluster_list[cluster_index][0], problem_num, list_value]
                error_list.append([final_df.iloc[cluster_index][problem_num], list_value])
                packing_lists.append(packing_list)
            else:
                packing_list = [cluster_list[cluster_index][0], problem_num, 0]
                error_list.append([final_df.iloc[cluster_index][problem_num], 0])
                packing_lists.append(packing_list)

    return packing_lists, error_list


# 3. ["*", "*"]인 환자를 찾기
indexs_list = []
for index_idx in range(len(val_df.index)):
    new_list = [-1,[]]
    for column_idx in range(len(val_df.columns)):
        #df 모든 곳을 돌면서 -1을 찾기(인덱스도 같이 잡아두기)
        if val_df.iloc[index_idx][column_idx] == ['*', '*']:
            new_list[0] = index_idx
            new_list[1].append(column_idx)
    if new_list[0] != -1:
        indexs_list.append(new_list)
packing_lists, error_list = find_value_for_packing(indexs_list)
print(error_list)


# 5. MAE 구하기
error_sum = [0., 0.]
for error in error_list:
    if error[0][0] >= error[1][0]:
        error_val_1 = error[0][0] - error[1][0]
    else:
        error_val_1 = error[1][0] - error[0][0]

    if error[0][1] >= error[1][1]:
        error_val_2 = error[0][1] - error[1][1]
    else:
        error_val_2 = error[1][1] - error[0][1]

    final_error = [error_val_1, error_val_2]
    error_sum[0] += final_error[0]
    error_sum[1] += final_error[1]

error_sum[0] /= len(error_list)
error_sum[1] /= len(error_list)

print("MAE: ", error_sum)
