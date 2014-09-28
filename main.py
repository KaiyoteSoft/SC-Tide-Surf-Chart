import pygame, sys
import urllib2
import json
import time
import datetime
# from datetime import datetime
from pygame.locals import *

try:
    import android
except ImportError:
    android = None

pygame.init()

if android:
    android.init()
    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)


screen_x = 1280
screen_y = 770
windowSurface = pygame.display.set_mode((screen_x, screen_y))


WHITE = ((255, 255, 255))
BLUE = ((85, 191, 223))
RED = ((255, 0, 0))


### gets the current day

change_day = 0

redraw = False
internet_connection = True

try :
    stri = "https://www.google.co.in"
    # info = urllib2.urlopen("http://api.spitcast.com/api/county/tide/santa-cruz/?")
    # info = urllib2.urlopen("http://api.spitcast.com/api/spot/forecast/147)")
    data = urllib2.urlopen(stri)
    print "Connected"
    internet_connection = True
except IOError:
    print "not connected"
    internet_connection = False


def get_date(delta_day = 0):
    """
    Creates the date string by receiving days it has to forecast
    :param delta_day:
    :return: date_string
    """
    change_time = datetime.datetime.now()
    change_time = change_time + datetime.timedelta(days=delta_day)
    month = str(change_time.month)
    day = str(change_time.day)
    if len(month) < 2:
        month = str(0) + month
    if len(day) < 2:
        day = str(0) + day

    date_string = str(change_time.year) + month + day
    return(date_string)

if internet_connection == True:
    ## open, read, load the tide
    def get_tide(date_string):
        """
        Recevies date_string and forecasts the tide
        :param date_string:
        :return: date, j_data
        """

        spit_date = get_date(date_string)
        info = urllib2.urlopen("http://api.spitcast.com/api/county/tide/santa-cruz/? dval={}".format(spit_date))
        data = info.read()
        j_data = json.loads(data)
        date = (j_data[0]["date"])

        return(date, j_data)

    def get_graph(j_data):
        """
        Gets j_data and constructs the points needed for the graph
        :param j_data:
        :return: point_list, time_labels, time_axis
        """
        x = 10
        draw_line = True
        point_list = []
        time_labels = []
        time_axis = []
        for tide_number in range(1, 25):
            j_tide = screen_y - int((j_data[tide_number]["tide"]) * 66 + 73)
            y = j_tide
            j_time = (j_data[tide_number]["hour"])
            j_time = (j_data[tide_number]["hour"])
            print(x, y)
            x = x + 49
            point_list.append((x, y))
            if draw_line == True:
                time_font = font.render("{}".format(j_time), True, BLUE)
                time_rect = (x, 720, 30, 20)
                pygame.draw.line(windowSurface, WHITE, (x, 250), (x, 700))
                draw_line = False
                time_labels.append(time_font)
                time_axis.append(time_rect)

            else:
                draw_line = True

        return(point_list, time_labels, time_axis)

    def get_condition(date_string):
        surf_date = get_date(date_string)
        hook_id = 147
        info = urllib2.urlopen(("http://api.spitcast.com/api/spot/forecast/{}/?dval={}".format(hook_id, surf_date)))
        data = info.read()
        j_surf_data = json.loads(data)
        break_data = (j_surf_data[0]["shape_full"])

        return(break_data)

    def get_surf(date_string):
        surf_date = get_date(date_string)
        hook_id = (147)

        info = urllib2.urlopen("http://api.spitcast.com/api/spot/forecast/{}/?dval={}".format(hook_id, surf_date))
        data = info.read()
        j_surf_data = json.loads(data)
        surf_data = round((j_surf_data[6]["size_ft"]), 1)

        return(surf_data)

    def get_capitola_surf(date_string):
        surf_date = get_date(date_string)
        capitola_id = (149)
        info = urllib2.urlopen("http://api.spitcast.com/api/spot/forecast/{}/?dval={}".format(capitola_id, surf_date))
        data = info.read()
        j_surf_data = json.loads(data)
        surf_data_2 = round((j_surf_data[6]["size_ft"]), 1)

        return(surf_data_2)

    def get_steamer_surf(date_string):
        surf_date = get_date(date_string)
        steamer_lane_id = (2)
        info = urllib2.urlopen("http://api.spitcast.com/api/spot/forecast/{}/?dval={}".format(steamer_lane_id, surf_date))
        data = info.read()
        j_surf_data = json.loads(data)
        surf_data_3 = round((j_surf_data[6]["size_ft"]), 1)

        return(surf_data_3)

    def get_pleasure_surf(date_string):
        surf_date = get_date(date_string)
        pleasure_point_id = (1)
        info = urllib2.urlopen("http://api.spitcast.com/api/spot/forecast/{}/?dval={}".format(pleasure_point_id, surf_date))
        data = info.read()
        j_surf_data = json.loads(data)
        surf_data_4 = round((j_surf_data[6]["size_ft"]), 1)

        return(surf_data_4)

    # instantiates functions
    date_string = get_date()
    date, j_data = get_tide(change_day)
    # date, j_data_2 = get_tide(change_day)

    break_data = get_condition(change_day)
    surf_data = get_surf(change_day)
    surf_data_2 = get_capitola_surf(change_day)
    surf_data_3 = get_steamer_surf(change_day)
    surf_data_4 = get_pleasure_surf(change_day)


    ## load fonts
    font = pygame.font.Font("fonts/animeace2_reg.ttf", 15)
    header_font = pygame.font.Font("fonts/animeace2_reg.ttf", 25)
    large_font = pygame.font.Font("fonts/animeace2_reg.ttf", 35)

    one_tide = font.render("1 ft", True, WHITE)
    one_rect = pygame.Rect(1220, 624, 50, 30)
    second_tide = font.render("2 ft", True, WHITE)
    second_rect = pygame.Rect(1220, 558, 50, 30)
    third_tide = font.render("3 ft", True, WHITE)
    third_rect = pygame.Rect(1220, 492, 50, 30)
    fourth_tide = font.render("4 ft", True, WHITE)
    fourth_rect = pygame.Rect(1220, 426, 50, 30)
    fifth_tide = font.render("5 ft", True, WHITE)
    fifth_rect = pygame.Rect(1220, 360, 50, 30)
    sixth_tide = font.render("6 ft", True, WHITE)
    sixth_rect = pygame.Rect(1220, 294, 100, 50)

        ################### Rectangles for surf
    date_font = large_font.render("The date is {}".format(date), True, WHITE)
    date_rect = pygame.Rect(250, 10, 700, 43)
    day_rect = pygame.Rect(1000, 20, 220, 80)
    ####### CENTERING THE TEXT
    day_text = header_font.render("DAY + 1", True, BLUE)
    day_pos = day_text.get_rect()
    day_pos.centerx = day_rect.centerx
    day_pos.centery = day_rect.centery

    reset_text = header_font.render("RESET", True, WHITE)
    reset_rect = pygame.Rect(1000, 160, 220, 80)
    reset_pos = reset_text.get_rect()
    reset_pos.centerx = reset_rect.centerx
    reset_pos.centery = reset_rect.centery

    ###
    condition_text = header_font.render("The Conditions are: {}".format(break_data), True, BLUE)
    condition_rect = pygame.Rect(420, 80, 400, 30)

    surf_text = header_font.render("The Hook: {} ft".format(surf_data), True, WHITE)
    surf_rect = pygame.Rect(30, 100, 300, 300)

    capitola_text = header_font.render("Capitola: {} ft".format(surf_data_2), True, BLUE)
    capitola_rect = pygame.Rect(30, 150, 300, 300)

    steamer_text = header_font.render("Steamer Lane: {} ft". format(surf_data_3), True, WHITE)
    steamer_rect = pygame.Rect(30, 200, 300, 300)

    pleasure_text = header_font.render("Pleasure Point: {} ft".format(surf_data_4), True, WHITE)
    pleasure_rect = pygame.Rect(320, 130, 300, 300)

    tide_title_text = large_font.render("Tide Table:", True, BLUE)
    tide_title_rect = pygame.Rect(450, 210, 240, 50)

    x = 10
    draw_line = True
    x_screen = 750
    point_list = []
    y_axis_start = []
    y_axis_end = []


    point_list, time_labels, time_axis = get_graph(j_data)

x_font = pygame.font.Font("fonts/SketchRockwell-Bold.ttf", 80)
no_connection_text = x_font.render("Sorry, No Internet Connection", True, BLUE)
no_connection_text_2 = x_font.render("Try Again Later", True, BLUE)
no_connection_rect = pygame.Rect(10, 200, 400, 400)
no_connection_rect_2 = pygame.Rect(300, 400, 400, 400)
    ####################






if internet_connection == False:
    while True:
        if android:
            if android.check_pause():
                android.wait_for_resume()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        windowSurface.fill(WHITE)
        windowSurface.blit(no_connection_text, no_connection_rect)
        windowSurface.blit(no_connection_text_2, no_connection_rect_2)
        pygame.display.update()

if internet_connection == True:

    while True:
        if android:
            if android.check_pause():
                android.wait_for_resume()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            mouse_pos = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONDOWN:
                if day_rect.collidepoint(mouse_pos):
                    windowSurface.fill((0,0,0))

                    redraw = True
                    change_day = change_day + 1
                    date, j_data = get_tide(change_day)

                if reset_rect.collidepoint(mouse_pos):
                    windowSurface.fill((0, 0, 0))
                    redraw = True
                    change_day = 0
                    date, j_data = get_tide(change_day)

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    #### If the day + 1 button is clicked, redraw screen
        if redraw == True:
            point_list, time_labels, time_axis = get_graph(j_data)
            redraw = False

        for y_tide in range(300, 699, 66):
            pygame.draw.line(windowSurface, BLUE, (10, y_tide), (1190, y_tide))
        pygame.draw.lines(windowSurface, WHITE, False, (point_list))
        pygame.draw.line(windowSurface, BLUE, (10, 500), (1190, 500), 5)

        index = 0
        for label in time_labels:
            windowSurface.blit(label, time_axis[index])
            index = index + 1

        windowSurface.blit(one_tide, one_rect)
        windowSurface.blit(second_tide, second_rect)
        windowSurface.blit(third_tide, third_rect)
        windowSurface.blit(fourth_tide, fourth_rect)
        windowSurface.blit(fifth_tide, fifth_rect)
        windowSurface.blit(sixth_tide, sixth_rect)
        windowSurface.blit(tide_title_text, tide_title_rect)
        pygame.draw.line(windowSurface, WHITE, tide_title_rect.bottomleft, tide_title_rect.bottomright, 3)

    ##### redrawing the date and all surf forecasts #########
        date_font = large_font.render("The date is {}".format(date), True, WHITE)
        windowSurface.blit(date_font, date_rect)
        pygame.draw.line(windowSurface, BLUE, date_rect.bottomleft, date_rect.bottomright, 3)

        surf_data = get_surf(change_day)
        surf_data_2 = get_capitola_surf(change_day)
        surf_data_3 = get_steamer_surf(change_day)
        surf_data_4 = get_pleasure_surf(change_day)

        condition_text = header_font.render("The Conditions are: {}".format(break_data), True, BLUE)
        surf_text = header_font.render("The Hook: {} ft". format(surf_data), True, WHITE)
        capitola_text = header_font.render("Capitola: {} ft".format(surf_data_2), True, BLUE)
        steamer_text = header_font.render("Steamer Lane: {} ft".format(surf_data_3), True, WHITE)
        pleasure_text = header_font.render("Pleasure Point: {} ft".format(surf_data_4), True, WHITE)
        windowSurface.blit(condition_text, condition_rect)
        windowSurface.blit(capitola_text, capitola_rect)
        windowSurface.blit(surf_text, surf_rect)
        windowSurface.blit(steamer_text, steamer_rect)
        windowSurface.blit(pleasure_text, pleasure_rect)
        pygame.draw.line(windowSurface, WHITE, condition_rect.bottomleft, condition_rect.bottomright, 3)

        windowSurface.blit(day_text, day_pos)
        windowSurface.blit(reset_text, reset_pos)
        pygame.draw.rect(windowSurface, WHITE, day_rect, 1)
        pygame.draw.rect(windowSurface, BLUE, reset_rect, 1)

        # print(day)
        pygame.display.update()







