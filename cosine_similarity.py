import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# 클러스터링을 위해 pickle파일 불러오기- 정/오답률, 평균시간
final_df_for_clustering_algorithm = pd.read_pickle("final_df_for_clustering_algorithm.pkl")


def patient_cosine_similarity_flatten():
    # 환자 기반 코사인 유사도 metrics(correct_rate, flatten O)
    df_for_cosine_similarity_correct_rate = pd.read_pickle("df_for_cosine_similarity_correct_rate.pkl")
    df_for_cosine_similarity_correct_rate_T = df_for_cosine_similarity_correct_rate.transpose()

    patient_cosine_similarity_correct_rate_result = cosine_similarity(df_for_cosine_similarity_correct_rate,
                                                                      df_for_cosine_similarity_correct_rate)
    patient_cosine_similarity_correct_rate = pd.DataFrame(patient_cosine_similarity_correct_rate_result,
                                                          index=df_for_cosine_similarity_correct_rate_T.columns,
                                                          columns=df_for_cosine_similarity_correct_rate_T.columns)

    # 환자 기반 코사인 유사도 metrics(time_response, flatten O)
    df_for_cosine_similarity_time_response = pd.read_pickle("df_for_cosine_similarity_time_response.pkl")
    df_for_cosine_similarity_time_response_T = df_for_cosine_similarity_time_response.transpose()

    patient_cosine_similarity_time_response_result = cosine_similarity(df_for_cosine_similarity_time_response,
                                                                       df_for_cosine_similarity_time_response)
    patient_cosine_similarity_time_response = pd.DataFrame(patient_cosine_similarity_time_response_result,
                                                           index=df_for_cosine_similarity_time_response_T.columns,
                                                           columns=df_for_cosine_similarity_time_response_T.columns)

    patient_cosine_similarity_flatten = patient_cosine_similarity_correct_rate + patient_cosine_similarity_time_response
    patient_cosine_similarity_flatten /= 2
    return patient_cosine_similarity_flatten


patient_cosine_similarity_flatten().to_pickle("patient_cosine_similarity_flatten.pkl")


def problem_cosine_similarity_flatten():
    # 문항 기반 코사인 유사도 metrics(correct_rate, flatten O)
    df_for_cosine_similarity_correct_rate = pd.read_pickle("df_for_cosine_similarity_correct_rate.pkl")
    df_for_cosine_similarity_correct_rate_T = df_for_cosine_similarity_correct_rate.transpose()

    problem_cosine_similarity_correct_rate_result = cosine_similarity(df_for_cosine_similarity_correct_rate_T,
                                                                      df_for_cosine_similarity_correct_rate_T)
    problem_cosine_similarity_correct_rate = pd.DataFrame(problem_cosine_similarity_correct_rate_result,
                                                          index=df_for_cosine_similarity_correct_rate.columns,
                                                          columns=df_for_cosine_similarity_correct_rate.columns)

    # 문항 기반 코사인 유사도 metrics(time_response, flatten O)
    df_for_cosine_similarity_time_response = pd.read_pickle("df_for_cosine_similarity_time_response.pkl")
    df_for_cosine_similarity_time_response_T = df_for_cosine_similarity_time_response.transpose()

    problem_cosine_similarity_time_response_result = cosine_similarity(df_for_cosine_similarity_time_response_T,
                                                                       df_for_cosine_similarity_time_response_T)
    problem_cosine_similarity_time_response = pd.DataFrame(problem_cosine_similarity_time_response_result,
                                                           index=df_for_cosine_similarity_time_response.columns,
                                                           columns=df_for_cosine_similarity_time_response.columns)

    problem_cosine_similarity_flatten = problem_cosine_similarity_correct_rate + problem_cosine_similarity_time_response
    problem_cosine_similarity_flatten /= 2
    return problem_cosine_similarity_flatten


problem_cosine_similarity_flatten().to_pickle("problem_cosine_similarity_flatten.pkl")