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

screen_x = 1280
screen_y = 770
windowSurface = pygame.display.set_mode((screen_x, screen_y))

WHITE = ((255, 255, 255))

### gets the current day

change_day = 0
redraw = False

def delta(delta_day = 0):
    change_time = datetime.datetime.now()
    change_time = change_time + datetime.timedelta(days=delta_day)
    month = str(change_time.month)
    day = str(change_time.day)
    if len(month) < 2:
        month = str(0) + month
    if len(day) < 2:
        day = str(0) + day

    change_date = str(change_time.year) + month + day
    print(change_date)

## open, read, load the tide
    info = urllib2.urlopen("http://api.spitcast.com/api/county/tide/santa-cruz/? dval={}".format(change_date))
    data = info.read()
    j_data = json.loads(data)
    date = (j_data[0]["date"])

    return(date, j_data)

# current_time = time.ctime(date)
date, j_data = delta()

## load fonts
font = pygame.font.Font("fonts/animeace2_reg.ttf", 15)
header_font = pygame.font.Font("fonts/animeace2_reg.ttf", 25)
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
    ###################
date_font = header_font.render("The date is {}".format(date), True, WHITE)
date_rect = pygame.Rect(250, 10, 300, 300)
day_text = header_font.render("DAY + 1", True, WHITE)
day_rect = pygame.Rect(1000, 20, 110, 35)
reset_text = header_font.render("RESET", True, WHITE)
reset_rect = pygame.Rect(1000, 100, 100, 35)


x = 10
draw_line = True
x_screen = 750
point_list = []
y_axis_start = []
y_axis_end = []

# def draw_window():

for tide_number in range(1, 25):
    j_tide = screen_y - int((j_data[tide_number]["tide"]) * 66 + 73)
    y = j_tide
    j_time = (j_data[tide_number]["hour"])
    print(x, y)
    x = x + 49
    point_list.append((x, y))
    if draw_line == True:
        time_font = font.render("{}".format(j_time), True, WHITE)
        time_rect = (x, 720, 30, 20)
        pygame.draw.line(windowSurface, WHITE, (x, 250), (x, 700))
        windowSurface.blit(time_font, time_rect)
        draw_line = False

    else:
        draw_line = True

# draw_window = draw_window()

while True:
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
                date, j_data = delta(change_day)

            if reset_rect.collidepoint(mouse_pos):
                windowSurface.fill((0, 0, 0))
                redraw = True
                change_day = 0
                date, j_data = delta(change_day)

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()


    if redraw == True:
        x = 10
        point_list = []
        for tide_number in range(1, 25):
            j_tide = screen_y - int((j_data[tide_number]["tide"]) * 66 + 73)
            y = j_tide
            j_time = (j_data[tide_number]["hour"])
            print(x, y)
            x = x + 49
            point_list.append((x, y))
            if draw_line == True:
                time_font = font.render("{}".format(j_time), True, WHITE)
                time_rect = (x, 720, 30, 20)

                pygame.draw.line(windowSurface, WHITE, (x, 250), (x, 700))
                windowSurface.blit(time_font, time_rect)
                date_font = header_font.render("The date is {}".format(date), True, WHITE)
                draw_line = False

            else:
                draw_line = True
        redraw = False

    for y_tide in range(300, 699, 66):
        pygame.draw.line(windowSurface, WHITE, (10, y_tide), (1190, y_tide))
    pygame.draw.lines(windowSurface, WHITE, False, (point_list))
    windowSurface.blit(one_tide, one_rect)
    windowSurface.blit(second_tide, second_rect)
    windowSurface.blit(third_tide, third_rect)
    windowSurface.blit(fourth_tide, fourth_rect)
    windowSurface.blit(fifth_tide, fifth_rect)
    windowSurface.blit(sixth_tide, sixth_rect)

    windowSurface.blit(date_font, date_rect)
    windowSurface.blit(day_text, day_rect)
    windowSurface.blit(reset_text, reset_rect)
    pygame.draw.rect(windowSurface, WHITE, day_rect, 1)
    pygame.draw.rect(windowSurface, WHITE, reset_rect, 1)

    # print(day)
    pygame.display.update()

