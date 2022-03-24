import os
import datetime
from astropy import units as u
import time
import sys

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

from astropy import coordinates as coord
from astropy import units as u
from astropy.time import Time
from astropy import time
import datetime
import pymap3d as pm

from Circle3D import Circle3D
from Point3D import Point3D

import coordinate_convertor




def ecef_to_j2000(target_time, *xyz):
    loc = pm.ecef2eci(*xyz, target_time)
    return loc

def j2000_to_ecef(current_time, *xyz):
    loc = pm.eci2ecef(*xyz, current_time)
    return loc

def convert_eci_time(start_time, target_time, xyz_list, sec_list):
    converted_xyz_list = []
    current_time = start_time
    for i in range(len(sec_list) - 1):
        current_xyz = xyz_list[i]
        ecef_xyz = j2000_to_ecef(
            current_time, *current_xyz)
        target_eci_xyz = ecef_to_j2000(
            target_time, *ecef_xyz)
        converted_xyz_list.append(target_eci_xyz)

        if sec_list[i+1] == None:
            break
        else:
            tick = float(sec_list[i+1])-float(sec_list[i])

        current_time += datetime.timedelta(seconds=tick)
        target_time += datetime.timedelta(seconds=tick)

        if(len(converted_xyz_list) > 5700):
            break
    return converted_xyz_list


def make_txt_file(converted_xyz_list, sec_list, isoformatTime):
    print(len(sec_list))
    file_name = isoformatTime.replace(':', "_")
    f = open(
        f'/home/spacemap-web/SpaceMap/public/script/naro_J2000_converted.txt', 'w')
    f.write(f'%coordinate system: J2000 \n')
    f.write(f'%site: Naro Space Center \n')
    f.write(f'%epochtime: {isoformatTime}\n')
    for i in range(0, len(converted_xyz_list)):
        sec = int(float(sec_list[i]))
        x = converted_xyz_list[i][0]
        y = converted_xyz_list[i][1]
        z = converted_xyz_list[i][2]
        data = "{0} {1} {2} {3} \n".format(sec, x, y, z)
        f.write(data)
    f.close()


def converter(file_path, t_year, t_month, t_day, t_hour, t_min, t_sec):
    lauch_file = file_reader.FileReader()
    xyz_list, sec_list = lauch_file.read_file(file_path)
    print(len(sec_list))
    start_time = datetime.datetime(2021, 2, 17, 3, 0, 0)
    # t_year, t_month, t_day, t_hour, t_min, t_sec = 2021, 4, 7, 3, 0, 0
    target_time = datetime.datetime(
        t_year, t_month, t_day, t_hour, t_min, t_sec)
    converted_xyz_list = convert_eci_time(
        start_time, target_time, xyz_list, sec_list)
    isoformatTime = datetime.datetime(
        t_year, t_month, t_day, t_hour, t_min, t_sec).isoformat()
    make_txt_file(converted_xyz_list, sec_list, isoformatTime)
    print("Done!")


if __name__ == "__main__":
    header_one = "%coordinate system: J2000\n"
    header_two = "%epochtime: 2022-03-13T00:00:00"
    # os.chdir('/Users/SHChoi/Desktop/coop_tg')
    home_path = '/home/coop/COOP/assistant_tool/New_Path_Generator/'
    file_path = '/home/coop/COOP/assistant_tool/New_Path_Generator/naro_J2000_converted.txt'
    
    original_coordinate_xyz_list = []
    elapsed_times = []
    number_of_new_paths = 100

    maneuver_start_time = 1390
    maneuver_end_time = 1460

    xs = []
    ys = []
    zs = []
    
    with open(file_path) as file:
        for i, string_line in enumerate(file.readlines()):
            if string_line == '':
                break
            string_line = string_line.split('\t')
            s = (string_line[0]) 
            if s[0] == '%':
                continue
            coordinate_xyz = (float(string_line[1]),float(string_line[2]),float(string_line[3]))

            original_coordinate_xyz_list.append(coordinate_xyz)
            elapsed_times.append(s)

    
    # new_path ?

    for flight_time in [40]:
        new_path = [ list() for _ in range(number_of_new_paths)]
        for i, coordinate_xyz in enumerate(original_coordinate_xyz_list):
            if i > flight_time * 60:
                break
            if int(elapsed_times[i]) >= maneuver_start_time and int(elapsed_times[i]) <= maneuver_end_time:
                curr_x = original_coordinate_xyz_list[i][0]
                curr_y = original_coordinate_xyz_list[i][1]
                curr_z = original_coordinate_xyz_list[i][2]
                
                prev_i = i-1 if (i-1 > 0) else i
                prev_x = original_coordinate_xyz_list[prev_i][0]
                prev_y = original_coordinate_xyz_list[prev_i][1]
                prev_z = original_coordinate_xyz_list[prev_i][2]
                
                center = Point3D(curr_x, curr_y, curr_z)
                radius = 100000
                normal = Point3D(curr_x-prev_x, curr_y-prev_y, curr_z-prev_z)
                normal.normalize()

                circle = Circle3D(normal, center, radius)
                samples_on_circle = circle.samples(number_of_new_paths)
                # xs.append(curr_x)
                # ys.append(curr_y)
                # zs.append(curr_z)
                # xs.append(prev_x)
                # ys.append(prev_y)
                # zs.append(prev_z)
                for index_of_new_path in range(number_of_new_paths):
                    new_path[index_of_new_path].append([elapsed_times[i], samples_on_circle[index_of_new_path].xCoord(), samples_on_circle[index_of_new_path].yCoord(), samples_on_circle[index_of_new_path].zCoord()])
                    # if(len(xs) < number_of_new_paths):
                    if(i == maneuver_start_time):
                        print(elapsed_times[i], samples_on_circle[index_of_new_path].xCoord(), samples_on_circle[index_of_new_path].yCoord(), samples_on_circle[index_of_new_path].zCoord())
                        xs.append(
                        samples_on_circle[index_of_new_path].xCoord()  
                        )
                        ys.append(
                        samples_on_circle[index_of_new_path].yCoord()  
                        )
                        zs.append(
                        samples_on_circle[index_of_new_path].zCoord()  
                        )
                    elif(i == maneuver_end_time):
                        print(elapsed_times[i], samples_on_circle[index_of_new_path].xCoord(), samples_on_circle[index_of_new_path].yCoord(), samples_on_circle[index_of_new_path].zCoord())
                        xs.append(
                        samples_on_circle[index_of_new_path].xCoord()  
                        )
                        ys.append(
                        samples_on_circle[index_of_new_path].yCoord()  
                        )
                        zs.append(
                        samples_on_circle[index_of_new_path].zCoord()  
                        )
                        # eci_xyz = [samples_on_circle[index_of_new_path].xCoord(), samples_on_circle[index_of_new_path].yCoord(), samples_on_circle[index_of_new_path].zCoord()]
                        # current_time = datetime.datetime(2022, 3, 13, 0, 0, 0)
                        # current_time += datetime.timedelta(seconds=1000)
                        # origin_time = datetime.datetime(2022, 3, 13, 0, 0, 0)
                        # ecef_loc = coordinate_convertor.j2000_to_ecef(current_time, *eci_xyz)
                        # with open( str(i) + str(index_of_new_path) + '.txt', 'w') as file:    
                        #     for elapsed_time in range(0, 7800, 600):
                        #         target_time = origin_time + datetime.timedelta(seconds=elapsed_time)
                        #         converted_eci_loc = coordinate_convertor.ecef_to_j2000(target_time, *ecef_loc)
                        #         to_write = str(elapsed_time) + ", " + str(converted_eci_loc[0]) + ", " + str(converted_eci_loc[1]) + ", " + str(converted_eci_loc[2]) + "\n"
                        #         file.write(to_write)


                            
                    # if(i == 1100):
                    #     print(index_of_new_path, samples_on_circle[index_of_new_path].xCoord(), samples_on_circle[index_of_new_path].yCoord(), samples_on_circle[index_of_new_path].zCoord())
                    # new_path[index_of_new_path][1] = samples_on_circle[index_of_new_path].xCoord
                    # new_path[index_of_new_path][2] = samples_on_circle[index_of_new_path].yCoord
                    # new_path[index_of_new_path][3] = samples_on_circle[index_of_new_path].zCoord


            else:
                for index_of_new_path in range(number_of_new_paths):
                    new_path[index_of_new_path].append([elapsed_times[i], original_coordinate_xyz_list[i][0], original_coordinate_xyz_list[i][1], original_coordinate_xyz_list[i][2]])
                    # new_path[index_of_new_path][1] = original_coordinate_xyz_list[i][0]
                    # new_path[index_of_new_path][2] = original_coordinate_xyz_list[i][1]
                    # new_path[index_of_new_path][3] = original_coordinate_xyz_list[i][2]
            
        
        for i in range(number_of_new_paths):
            output_path = home_path + "/output/new_path_#" + str(i+1) + "_flight_time_" + str(flight_time) + ".txt"
            with open(output_path, 'w') as file:
                file.write(header_one)
                file.write(header_two)
                for text in new_path[i]:
                    file.write('\n')
                    file.write(str(text[0]) + '\t' + str(text[1]) + '\t' + str(text[2]) + '\t' + str(text[3]))
        

    fig = plt.figure(figsize=(16, 16))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xs, ys, zs, color="blue", marker='o', s=15, cmap='Greens')
    print(xs)
    plt.savefig('abc.png')
                    
