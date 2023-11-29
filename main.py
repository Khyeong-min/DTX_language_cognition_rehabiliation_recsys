import zenicog_rec_result
import random
import pandas as pd

#클러스터링을 위해 pickle파일 불러오기
final_df_for_clustering_algorithm = pd.read_pickle("final_df_for_clustering_algorithm.pkl")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("-------------------문항 추천 시스템------------------------\n")
    print("*********추천 받을 수 있는 추천 문항에 대한 설명**********")
    print("1. 본인의 정보가 아닌 유사한 환자의 정보만을 고려한 문항")
    print("2. 유사한 환자가 아닌 오직 본인의 정보만을 고려한 문항")
    print("3. 유사한 환자와 본인의 정보에서 동시에 추천하는 문항")
    print("****************************************************\n")

    bool_value = True
    patient_number = 2
    patient_code = final_df_for_clustering_algorithm.index[patient_number]

    print("환영합니다!", patient_code, "님")
    while bool_value:
        wanted_rec_type = int(input("원하는 추천 문항?(1,2,3이 아닌 숫자를 선택하면 종료됩니다.) "))
        if wanted_rec_type not in [1, 2, 3]:
            bool_value = False
        else:
            print("\n############## 추천 받을 문항 ##############")
            final_recommended_problem = zenicog_rec_result.return_final_recommended_problem(PatientCode= patient_code,
                                                                                            Wanted_rec_type=wanted_rec_type)
            for i, rec_problem in enumerate(final_recommended_problem):
                i += 1
                print(i, ":", rec_problem)
            print("###########################################\n")

    print("\n------------------문항 추천 시스템 종료-----------------------")


