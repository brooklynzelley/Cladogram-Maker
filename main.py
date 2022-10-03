import pygame as pg

# adds text boxes anywhere. Can link them by pressing shift+l into link mode.
# Four circles appear on all textboxes at top,right,bottom,left of their rects.
# When two of different boxes are pressed, (should highlight selected ones at
# key_down), they are automatically formatted. If it's right->left then it
# should be a horiszontal line of 100 length? If it's bottom->left, should be a
# line going down 50? and another connected on that one going right 75? to the
# other textbox. The textbox input should just be python input() when clicked
# and put at the point of click and all tree starting textboxes should always
# automatically be aligned, being 30? pixels down from the bottom of the one
# above. Also, there should be a way to use arrow keys to size up or down text
# and possibly move around with wasd (easily outside of input())

pg.init()
screen_width = 1440
screen_height = 900
screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
clock = pg.time.Clock()
font = pg.font.SysFont('menlo', 20)
CIRCLE_CONNECTOR_RADIUS = 10

class TextBox(pg.sprite.Sprite):
    def __init__(self, font, text, pos):
        super().__init__()
        self.image = font.render(text, True, (255,255,255))
        self.rect = self.image.get_rect(midleft=pos)
        ## self.link is either False / (pos1, pos2, from, next) / next
        ## no connections / has previous connection / only next connection
        # pos being top, left, bottom, right of prev and this sprite
        # from being prev connected sprite
        # next being next connected sprite or None
        self.link = False
        self.top_circle_surf = pg.Surface((CIRCLE_CONNECTOR_RADIUS*2,CIRCLE_CONNECTOR_RADIUS*2))
        pg.draw.circle(self.top_circle_surf, (200,200,0), (CIRCLE_CONNECTOR_RADIUS,CIRCLE_CONNECTOR_RADIUS), 10)

        self.right_circle_surf = pg.Surface((CIRCLE_CONNECTOR_RADIUS*2,CIRCLE_CONNECTOR_RADIUS*2))
        pg.draw.circle(self.right_circle_surf, (200,200,0), (CIRCLE_CONNECTOR_RADIUS,CIRCLE_CONNECTOR_RADIUS), 10)

        self.bottom_circle_surf = pg.Surface((CIRCLE_CONNECTOR_RADIUS*2,CIRCLE_CONNECTOR_RADIUS*2))
        pg.draw.circle(self.bottom_circle_surf, (200,200,0), (CIRCLE_CONNECTOR_RADIUS,CIRCLE_CONNECTOR_RADIUS), 10)

        self.left_circle_surf = pg.Surface((CIRCLE_CONNECTOR_RADIUS*2,CIRCLE_CONNECTOR_RADIUS*2))
        pg.draw.circle(self.left_circle_surf, (200,200,0), (CIRCLE_CONNECTOR_RADIUS,CIRCLE_CONNECTOR_RADIUS), 10)
        self.align_circles()

    def align_circles(self):
        self.top_circle_rect = self.top_circle_surf.get_rect(center=self.rect.midtop)
        self.right_circle_rect = self.right_circle_surf.get_rect(center=self.rect.midright)
        self.bottom_circle_rect = self.bottom_circle_surf.get_rect(center=self.rect.midbottom)
        self.left_circle_rect = self.left_circle_surf.get_rect(center=self.rect.midleft)

    def blit_to_screen(self):
        screen.blit(self.image, self.rect)
        if link_mode:
            screen.blit(self.top_circle_surf, self.top_circle_rect)
            screen.blit(self.right_circle_surf, self.right_circle_rect)
            screen.blit(self.bottom_circle_surf, self.bottom_circle_rect)
            screen.blit(self.left_circle_surf, self.left_circle_rect)


def draw_connected_textboxes(a, b):
    if b.link[0] == 'right' and b.link[1] == 'left':
        # we assume a is already in place
        a.blit_to_screen()
        # put the next sprite in the tree in position, with enough space to
        # draw the line
        b.rect.midleft = (a.rect.midright[0]+100, a.rect.midright[1])
        # re-align the connector circles
        b.align_circles()
        # show the text box
        b.blit_to_screen()
        # show the line
        pg.draw.line(screen, (255,255,255), a.rect.midright, b.rect.midleft)


def format_screen():
    tree_start_sprites = []
    start_tree_pos = [0, 50]
    for i in Textboxes.sprites():
        if type(i.link) == TextBox:
            # means it's the start of a tree
            tree_start_sprites.append(i)
            # start in right place
            i.rect.midleft = start_tree_pos
            # re-align the connector cicles
            i.align_circles()
            # show it as it won't move
            i.blit_to_screen()
            # change the position for next tree starting sprites
            start_tree_pos[1] += 50
        elif i.link == False:
            # this could go anywhere as it isn't connected and won't move so
            # print it where it is
            i.blit_to_screen()
            
    for i in tree_start_sprites:
        next_ = i.link
        # initiate a and b with the tree_start_sprite and it's second connection
        a = i
        b = next_
        # i.link[3] refers to i's next connected sprite
        # carry on until there is no more a.link[3]
        while not a.link == False:
            if type(a.link) == list and a.link[3] == None:
                break
            next_add = []
            # this draws both textboxes in the right place with the line between them
            draw_connected_textboxes(a, b)
            # move the sprites we are connecting along one
            a = b
            b = a.link[3]


def get_connector_circle(position):
    for i in Textboxes.sprites():
        if i.top_circle_rect.collidepoint(position):
            return [i, 'top']
        elif i.right_circle_rect.collidepoint(position):
            return [i, 'right']
        elif i.bottom_circle_rect.collidepoint(position):
            return [i, 'bottom']
        elif i.left_circle_rect.collidepoint(position):
            return [i, 'left']

    return None

def connect(circle1, circle2):
    # put them in the right order (order on tree)
    if circle1[1] == 'right' and circle2[1] == 'left':
        first_circle, second_circle = [circle1, circle2]
    elif circle1[1] == 'left' and circle2[1] == 'right':
        first_circle, second_circle = [circle2, circle1]

    first_sprite = first_circle[0]
    second_sprite = second_circle[0]

    # we always want to put second_sprite there but when it's a list we don't want to overwrite the previous link
    if type(first_sprite.link) == list:
        # next connected sprite
        first_sprite.link[3] = second_sprite
    else:
        first_sprite.link = second_sprite

    # the second sprite's link will always be a list type but it's next connection will be different case-by-case
    if second_sprite.link == False:
        next_connection = None
    elif type(second_sprite.link) == list:
        next_connection = second_sprite.link[3]
    else:
        next_connection = second_sprite.link
    second_sprite.link = [first_circle[1], second_circle[1], second_sprite, next_connection]


Textboxes = pg.sprite.Group()

link_mode = False
mode_show = font.render('link mode', True, (255,255,255))
mode_show_rect = mode_show.get_rect(midtop=(screen_width/2, 0))
clicked_positions = [(0,0), (0,0)]

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_l:
                link_mode = not link_mode
        if link_mode:
            if event.type == pg.MOUSEBUTTONDOWN:
                # add new position to end of clicked_positions while keeping it
                # 2 elements long
                clicked_positions = [clicked_positions[1], pg.mouse.get_pos()]
                # this ultimately changes self.link to what it needs to be
                circle1 = get_connector_circle(clicked_positions[0])
                circle2 = get_connector_circle(clicked_positions[1])
                if circle1 != None and circle2 != None:
                    connect(circle1, circle2)
                    #clicked_positions = [(0,0), (0,0)]
                else:
                    pass
                    #clicked_positions = [(0,0), (0,0)]
        elif not link_mode:
            if event.type == pg.MOUSEBUTTONDOWN:
                Textboxes.add(TextBox(font, input('Enter text: '), pg.mouse.get_pos()))


    screen.fill((0,0,0))

    if link_mode:
        screen.blit(mode_show, mode_show_rect)

    # draw all textboxes with links
    format_screen()

    pg.display.flip()
    clock.tick(60)
pg.quit()
