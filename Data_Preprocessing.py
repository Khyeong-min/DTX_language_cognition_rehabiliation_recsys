import pandas as pd

#엑셀 파일 불러오기
result_exel = pd.read_excel("제니코그_DF(연습).xlsx")
result_df = result_exel.to_csv("result_csv")
result_df = pd.read_csv('result_csv')
result_df.drop("Unnamed: 0", axis=1, inplace=True)

#문항번호 리스트 불러오기
df_for_clustering_algorithm_columns_list = []
txt_df = pd.read_table('문항번호 리스트.txt')
for i in txt_df.index:
    df_for_clustering_algorithm_columns_list.append(txt_df.loc[i]['문항번호리스트'])

# 새롭게 데이터 프레임을 만들 훈련 문항에 대한 리스트를 전달하는 함수
def return_problem_list():
    # 전달할 list
    problem_lists = []

    # csv 파일에 훈련이라는 column추가
    result_df["훈련"] = "problem"

    # CSV를 돌면서 훈련 column에 추가하기
    for patient_index in result_df.index:
        problem_list = []
        if patient_index != 0:
            problem_1 = result_df.loc[patient_index, "훈련대분류"]
            problem_2 = result_df.loc[patient_index, '훈련 중분류']
            problem_3 = result_df.loc[patient_index, '훈련유형']
            problem_4 = result_df.loc[patient_index, '단계(난이도)']
            problem_list = [problem_1, problem_2, problem_3, problem_4]
            problem_lists.append(problem_list)

    return result_df, problem_lists

# 훈련문제에 대한 것을 합쳐주고 데이터프레임 return
def make_next_df():
    # 문항 리스틀 전달받음- [[인지, 집행력, 다른 것 찾기, 1], [언어, 읽기, 의미-단어 매칭하기, 1],----]
    result_df, problem_lists = return_problem_list()
    for i, problem_list in enumerate(problem_lists):
        new_str = ""  # new_str은 problem column에 넣을 문항이름
        for list_element in problem_list:
            new_str += list_element
            new_str += "-"
        result_df.loc[i + 1]['훈련'] = new_str[:-1]

    # skip이 있는 행 삭제
    drop_case = result_df[result_df['skip여부'] == 'true'].index
    result_df.drop(drop_case, inplace=True)

    # 훈련 대분류~ skip 여부까지 모두 삭제
    result_df.drop(["훈련대분류", "훈련 중분류", "훈련유형", "단계(난이도)", "skip여부"], axis=1, inplace=True)

    return result_df


# 같은 문제에 대해 묶어서 평균 정오답 확률과 평균 반응시간을 계산후 return
def make_added_list():
    # 훈련 문제까지 합친 df
    result_df = make_next_df()
    # 훈련 column을 돌면서 다른 훈련 목록이 나오면 넘기기
    return_lists = []
    sum_iscorrected = 0.
    sum_time = 0.
    sum_count = 0

    for i, problem_index in enumerate(result_df["훈련"].index):
        if i != 0:
            # 문항의 인덱스 번호
            index_ = result_df.index[i]

            # 마지막 문제를 리스트에 더하고 마무리
            if problem_index == result_df["훈련"].index[-1]:
                if result_df['정답여부'][index_] == 'true':
                    sum_iscorrected += 1
                else:
                    sum_iscorrected += 0
                if result_df['반응시간'][index_].replace(',', '') != '[NULL]':
                    sum_time += float(result_df['반응시간'][index_].replace(',', ''))
                sum_count += 1
                return_list_1 = [index_, result_df['환자번호'][index_], sum_iscorrected / sum_count, sum_time / sum_count,
                               result_df['ICF_CODES (훈련유형에 종속)'][index_], result_df["훈련"][index_]]
                return_lists.append(return_list_1)

                return result_df, return_lists

            # 문항이 바뀌지 않으면- 같은 문제-> 정답, 시간, 횟수를 구해야 함-> 평균 정/오답률, 평균 시간을 구하기 위해
            if result_df["훈련"].loc[index_] == result_df["훈련"].loc[result_df.index[i + 1]]:
                if result_df['정답여부'][index_] == 'true':
                    sum_iscorrected += 1
                else:
                    sum_iscorrected += 0
                if result_df['반응시간'][index_].replace(',', '') != '[NULL]':
                    sum_time += float(result_df['반응시간'][index_].replace(',', ''))
                sum_count += 1
            # 문항이 바뀌면- 정/오답 합, 시간 합, 몇 문제, index번호 리스트 전달
            else:
                if result_df['정답여부'][index_] == 'true':
                    sum_iscorrected += 1
                else:
                    sum_iscorrected += 0
                if result_df['반응시간'][index_].replace(',', '') != '[NULL]':
                    sum_time += float(result_df['반응시간'][index_].replace(',', ''))
                sum_count += 1

                if sum_count != 0:
                    return_list_2 = [index_, result_df['환자번호'][index_], sum_iscorrected / sum_count, sum_time / sum_count,
                                   result_df['ICF_CODES (훈련유형에 종속)'][index_], result_df["훈련"][index_]]
                return_lists.append(return_list_2)

                sum_iscorrected = 0.  # 정오답 합 초기화
                sum_time = 0.  # 시간 합 초기화
                sum_count = 0  # 같은 문제 수 합 초기화


# 최종 데이터 테이블을 만들고 반환하는 함수
def make_merge_df():
    result_df, return_list = make_added_list()

    merged_df = result_df.drop(index=result_df.loc[result_df.index >= 1].index)
    merged_df.rename(columns={'정답여부': "정/오답 확률"}, inplace=True)
    merged_df.rename(columns={'반응시간': "평균 반응시간"}, inplace=True)
    for i, add_list in enumerate(return_list):
        if i == 0:
            pass
        merged_df.loc[i] = add_list[1:]

    return merged_df


# row는 환자번호, column은 훈련문제코드로 수정하는 함수
def make_df_for_clustering_algorithm():
    # 정/오답 확률, 평균 반응시간을 계산한 df를 return
    merged_df = make_merge_df()

    # 최종적으로 만들어질 df의 column값들을 담은 리스트를 return
    column_list = df_for_clustering_algorithm_columns_list

    df_for_clustering_algorithm = pd.DataFrame(index=merged_df['환자번호'].drop_duplicates(), columns=column_list)
    for index in merged_df.index:
        val_str = ""
        val_str += str(merged_df['정/오답 확률'].loc[index])
        val_str += "/"
        val_str += str(merged_df['평균 반응시간'].loc[index])
        df_for_clustering_algorithm.loc[merged_df['환자번호'].loc[index]][merged_df['훈련'].loc[index]] = val_str

    df_for_clustering_algorithm = df_for_clustering_algorithm.fillna("-1.0/-1.0")

    return df_for_clustering_algorithm


#최종적인 데이터 프레임 결과(flatten X)
def make_final_df_for_clustering_algorithm():
    df_for_clustering_algorithm = make_df_for_clustering_algorithm().copy()
    for index in df_for_clustering_algorithm.index:
        for column in df_for_clustering_algorithm.columns:
            list_value = df_for_clustering_algorithm[column].loc[index].split('/')
            list_value[0] = float(list_value[0])
            if list_value[1] == '-1.0':
                list_value[1] = float(list_value[1])
            else:
                list_value[1] = round((float(list_value[1]) / 1000), 1)
            df_for_clustering_algorithm.loc[index, column] = list_value
    return df_for_clustering_algorithm


final_df_for_clustering_algorithm = make_final_df_for_clustering_algorithm()

final_df_for_clustering_algorithm.to_pickle("final_df_for_clustering_algorithm.pkl")


# 코사인 유사도 metrics를 계산하기 위해 데이터프레임을 flatten하고 pickle파일에 저장
def final_df_for_cosine_similarity():
    df_for_clustering_algorithm = pd.read_pickle("final_df_for_clustering_algorithm.pkl")
    df_for_clustering_algorithm_1 = df_for_clustering_algorithm.copy()
    df_for_clustering_algorithm_2 = df_for_clustering_algorithm_1.copy()

    #평균 정/오답 확률 flatten
    for index_1 in df_for_clustering_algorithm_1.index:
        for column_1 in df_for_clustering_algorithm_1.columns:
            value_1 = df_for_clustering_algorithm_1[column_1].loc[index_1][0]
            df_for_clustering_algorithm_1.loc[index_1, column_1] = float(value_1)

    # 평균 소요시간 flatten
    for index_2 in df_for_clustering_algorithm_2.index:
        for column_2 in df_for_clustering_algorithm_2.columns:
            value_2 = df_for_clustering_algorithm_2[column_2].loc[index_2][1]
            df_for_clustering_algorithm_2.loc[index_2, column_2] = float(value_2)

    return df_for_clustering_algorithm_1, df_for_clustering_algorithm_2


df_for_cosine_similarity_correct_rate, df_for_cosine_similarity_time_response = final_df_for_cosine_similarity()
df_for_cosine_similarity_correct_rate.to_pickle("df_for_cosine_similarity_correct_rate.pkl")
df_for_cosine_similarity_time_response.to_pickle("df_for_cosine_similarity_time_response.pkl")


