import pandas as pd
import numpy as np
import os

from itertools import combinations
from scipy.io import arff
from src.utils import get_project_root

root = get_project_root()


class SeventhLab:
    def __init__(self):
        self.df = None
        self.df1 = None
        self.df2 = None
        self.filename = os.path.join(root, os.path.join('data', 'weather.arff'))
        self.exercise_01()
        self.exercise_02()
        self.exercise_03()
        self.exercise_04_05()

    def exercise_01(self):
        data, meta = arff.loadarff(self.filename)

        df1 = pd.DataFrame(data)
        df2 = pd.DataFrame(data).select_dtypes([np.object]).stack().str.decode('utf-8').unstack()

        self.df1 = df1.drop(columns=df2.select_dtypes([np.object]).columns)
        self.df = df2.join(self.df1)
        self.df2 = df2

    def exercise_02(self):
        df = self.df.dropna()
        self.df = df[df != "?"].dropna()

    def exercise_03(self):
        for col in self.df1:
            self.df[col] = pd.cut(
                self.df[col].values,
                [0, int(np.mean([min(self.df[col].values), max(self.df[col].values)])), max(self.df[col].values)]
            ).codes
        for col in self.df2:
            classes = np.unique(self.df[col])
            self.df[col] = [np.where(classes == weather)[0][0] for weather in self.df[col]]
        print(self.df)

    def exercise_04_05(self):
        lst = ['temperature', 'humidity', 'windy', 'play']
        rs_max = 0
        df_new = self.df

        while rs_max != 1.0:
            df_nconf = df_new.drop_duplicates(subset=lst, keep=False)  # consistent

            gamma_all = len(df_nconf) / len(df_new)
            print(f"Gamma for all: {gamma_all}")

            df_nconf_list = [df_new.drop_duplicates(subset=list(x), keep=False)
                             for x in combinations(lst, len(lst) - 1)]

            gammas = [len(el) / len(self.df) for el in df_nconf_list]
            for i, gamma in enumerate(gammas):
                print(f"Gamma {lst[i]}: {gamma}")

            rs = [(gamma_all - gamma) / gamma_all for gamma in gammas]
            for i, r in enumerate(rs):
                print(f"R {lst[i]}: {r}")

            df_new = self.df.drop([lst[min(range(len(rs)), key=rs.__getitem__)]], axis=1)
            lst.remove(lst[min(range(len(rs)), key=rs.__getitem__)])
            print(lst)
            rs_max = max(rs)

        print(f"-----\nReducer: {lst}")

    def exercise_06(self):
        df_certainty = self.df.drop_duplicates()  # -> if not duplicates
        # print(df.duplicated().value_counts())
        # print(df)
        # df_conflict = 0 # -> if duplicates.num ??
        # df_uncertainty = 0 # -> if duplicates.num ??

        # -- Ideas -- #
        # df2 = df.drop(["windy"], axis=1)
        # df_nconf2 = df2.drop_duplicates(subset=['temperature', 'humidity', 'play'], keep=False)  # consistent
        # gamma_all2 = len(df_nconf2) / len(df2)
        # print(f"Gamma for all: {gamma_all2}")
        #
        # lst2 = ['temperature', 'humidity', 'play']
        #
        # df_nconf_list2 = [df2.drop_duplicates(subset=list(x), keep=False) for x in combinations(lst2, len(lst2) - 1)]
        # gammas2 = [len(el) / len(df2) for el in df_nconf_list2]
        # for i, gamma in enumerate(gammas2):
        #     print(f"Gamma x{i}: {gamma}")
        # print()
        # rs2 = [(gamma_all - gamma) / gamma_all for gamma in gammas2]
        # for i, r in enumerate(rs2):
        #     print(f"R x{i}: {r}")
        #
        # df3 = df2.drop(["play"], axis=1)
        # df_nconf3 = df3.drop_duplicates(subset=['temperature', 'humidity'], keep=False)  # consistent
        # gamma_all3 = len(df_nconf3) / len(df3)
        # print(f"Gamma for all: {gamma_all3}")
        #
        # lst3 = ['temperature', 'humidity']
        #
        # df_nconf_list3 = [df3.drop_duplicates(subset=list(x), keep=False) for x in combinations(lst3, len(lst3) - 1)]
        # gammas3 = [len(el) / len(df3) for el in df_nconf_list3]
        # for i, gamma in enumerate(gammas3):
        #     print(f"Gamma x{i}: {gamma}")
        # print()
        # rs3 = [(gamma_all - gamma) / gamma_all for gamma in gammas3]
        # for i, r in enumerate(rs3):
        #     print(f"R x{i}: {r}")

        # data_frame_1 = 0 # -> conflict -> if duplicates.num ??
        # data_frame_2 = 0 # -> uncertainty -> if duplicates.num ??
        # data_frame_3 = 0 # -> certainty -> if not duplicates
