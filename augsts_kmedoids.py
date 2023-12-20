import kmedoids
import numpy
from openpyxl import load_workbook
from openpyxl import Workbook
import time
import math
import random

dist_data = numpy.load("augSTS_numpy_save.npy")
test_data = numpy.load("augSTS_test_numpy_save.npy")
#num_cluster 34, random_state 16

#dist_data = numpy.load("sbert_numpy_save.npy")
#test_data = numpy.load("sbert_test_numpy_save.npy")
#num_cluster 35, random_state 9

#dist_data = numpy.load("MiniLM_numpy_save.npy")
#test_data = numpy.load("MiniLM_test_numpy_save.npy")
#num_cluster 36, random_state 4


num_cluster = [34]
random_state = [16]

for num_c in num_cluster:
    for rand_s in random_state:
        km = kmedoids.KMedoids(num_c, method='fasterpam', random_state = rand_s, max_iter=300)

        c = km.fit(dist_data)
        result_np = c.predict(dist_data)
        test_np = c.predict(test_data)
        result = result_np.tolist()
        test = test_np.tolist()

        all_num = 0
        all_real = 0
        real_collected = 0
        real_gpt = 0
        all_fake = 0
        fake_collected = 0
        fake_gpt = 0

        Fakes = []
        Trues = []

        check = []
        all_indexes = [[] for i in range(num_c)]
        for i in range(num_c): check.append([0, 0])

        for i in range(len(result)):
            all_indexes[result[i]].append(i)
            if(result[i] == 22):
                print(i)
            if(i < 9235):
                check[result[i]][0] += 1
            else:
                check[result[i]][1] += 1

        for i in range(len(check)):

            if(check[i][0] <= check[i][1]):
                Fakes.append(i)
                all_fake += check[i][0]
                all_fake += check[i][1]
                fake_collected += check[i][0]
                fake_gpt += check[i][1]

            else:
                Trues.append(i)
                all_real += check[i][0]
                all_real += check[i][1]
                real_collected += check[i][0]
                real_gpt += check[i][1]
        test_result = []
        print(check)
        print(test)

        for i in range(num_c): test_result.append([0, 0])

        test_fake_real = [0, 0]

        for i in range(len(test)):
            test_result[test[i]][0] += 1
            if(test[i] in Trues):
                test_fake_real[1] += 1
            else:
                test_fake_real[0] += 1

        print(c.medoid_indices_)
        all_num = all_real + all_fake
        sampling_size = 641.0 / 18468.0
        sampled_index = [[] for i in range(num_c)]
        for i in range(len(all_indexes)):
            cluster_sample_size = round(len(all_indexes[i])*sampling_size)
            print(cluster_sample_size, "---", i)
            sampled_index[i].append(c.medoid_indices_[i])
            while(len(sampled_index[i]) < cluster_sample_size):
                val = random.choice(all_indexes[i])
                if(val not in sampled_index[i]):
                    sampled_index[i].append(val)
        print(sampled_index)

        """
        workbook = load_workbook("all_data.xlsx")
        worksheet = workbook['output']
        for counter in range(len(sampled_index)):
            for index in sampled_index[counter]:

                worksheet["H"+str(int(index)+2)] = counter
        

        workbook.save("all_data.xlsx")
        """

        if(fake_gpt / all_num > 0.46 and test_fake_real[1] / 20 >= 0.75):
            print(num_c, rand_s)
            print("Loss is:", num_c, " , ", c.inertia_)
            print("all data : ", all_real + all_fake)
            print("predicted Real : ", all_real/ all_num)
            print(real_collected / all_num)
            print(real_gpt / all_num)
            print("------------")
            print("predicted Fake : ", all_fake/all_num)
            print(fake_collected / all_num)
            print(fake_gpt / all_num)
            print(test_fake_real[1] / 20)


