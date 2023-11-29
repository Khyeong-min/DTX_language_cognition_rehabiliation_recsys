from zenicog_rec_algorithm import rec_system_1, rec_system_2
import pandas as pd

# 클러스터링을 위해 pickle파일 불러오기
final_df_for_clustering_algorithm = pd.read_pickle("final_df_for_clustering_algorithm.pkl")


def return_final_recommended_problem_list(PatientCode):
    # 최종 추천 문항 리스트
    duplicated_problem_list = []

    # 첫번째 추천 알고리즘을 통한 결과
    not_solved_problem_list = rec_system_1(PatientCode)
    # 두번째 추천 알고리즘을 통한 결과
    customized_problem_list = rec_system_2(PatientCode)

    # 중복된 값만을 최종문항 리스트로 제안
    if len(customized_problem_list) <= len(not_solved_problem_list):
        for i in range(len(customized_problem_list) - 1):
            for k in range(len(customized_problem_list) - 1):
                if int(customized_problem_list[i]) == int(not_solved_problem_list[k]):
                    duplicated_problem_list.append(customized_problem_list[i])
    else:
        for i in range(len(not_solved_problem_list) - 1):
            for k in range(len(not_solved_problem_list) - 1):
                if int(customized_problem_list[i]) == int(not_solved_problem_list[k]):
                    duplicated_problem_list.append(not_solved_problem_list[i])

    return not_solved_problem_list, customized_problem_list, duplicated_problem_list


# 사용자가 wanted_rec_type를 1번을 선택할 때- 유사한 환자들이 풀었던 문항 정보
def return_final_recommended_problem_1(not_solved_problem_list):
  final_recommended_problem = []
  for cnt, problem_name in enumerate(final_df_for_clustering_algorithm.columns):
      if cnt in not_solved_problem_list:
        final_recommended_problem.append(problem_name)
      list_index = 0
      count = 0
      for rec_problem in final_recommended_problem:
        if count < (len(final_recommended_problem)-2):
          if list_index == 0:
            list_index += 1
            pass
          else:
            if final_recommended_problem[list_index][:-2] == final_recommended_problem[list_index-1][:-2]:
              final_recommended_problem.remove(final_recommended_problem[list_index])
            else:
              list_index += 1
        count += 1
  return final_recommended_problem


# 사용자가 wanted_rec_type를 2번을 선택할 때- 내 문항 정보
def return_final_recommended_problem_2(customized_problem_list):
  final_recommended_problem = []
  for cnt, problem_name in enumerate(final_df_for_clustering_algorithm.columns):
      if cnt in customized_problem_list:
        final_recommended_problem.append(problem_name)
      list_index = 0
      count = 0
      for rec_problem in final_recommended_problem:
        if count < (len(final_recommended_problem)-2):
          if list_index == 0:
            list_index += 1
            pass
          else:
            if final_recommended_problem[list_index][:-2] == final_recommended_problem[list_index - 1][:-2]:
              final_recommended_problem.remove(final_recommended_problem[list_index])
            else:
              list_index += 1
        count += 1
  return final_recommended_problem


# 사용자가 wanted_rec_type를 3번을 선택할 때- 중복되는 정보
def return_final_recommended_problem_3(duplicated_problem_list):
  final_recommended_problem = []
  for cnt, problem_name in enumerate(final_df_for_clustering_algorithm.columns):
      if cnt in duplicated_problem_list:
        final_recommended_problem.append(problem_name)
      list_index = 0
      count = 0
      for rec_problem in final_recommended_problem:
        if count < (len(final_recommended_problem)-2):
          if list_index == 0:
            list_index += 1
            pass
          else:
            if final_recommended_problem[list_index][:-2] == final_recommended_problem[list_index-1][:-2]:
              final_recommended_problem.remove(final_recommended_problem[list_index])
            else:
              list_index += 1
        count += 1
  return final_recommended_problem


# 최종 추천 문항을 출력
def return_final_recommended_problem(PatientCode, Wanted_rec_type):
    final_recommended_problem = []
    not_solved_problem_list, customized_problem_list, duplicated_problem_list = return_final_recommended_problem_list(PatientCode)
    if Wanted_rec_type == 1:
        final_recommended_problem = return_final_recommended_problem_1(not_solved_problem_list)

    if Wanted_rec_type == 2:
        final_recommended_problem = return_final_recommended_problem_2(customized_problem_list)

    if Wanted_rec_type == 3:
        final_recommended_problem = return_final_recommended_problem_3(duplicated_problem_list)

    return final_recommended_problem