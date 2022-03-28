import pygame

black, green, red, blue, yellow = (0, 0, 0), (0, 250, 100), (200, 0, 0), (0, 0, 200), (200, 200, 0)

class Visualizer(object):
    def __init__(self,max_x, max_y,instance,model_solver):
        self.max_x,self.max_y=max_x,max_y
        self.ButtonCoordinates()
        self.instance=instance
        self.model_solver=model_solver
        self.done = False

    def ButtonCoordinates(self):
        self.button_size=50
        self.button_x1=(self.max_x-self.button_size)/2
        self.button_x2=(self.max_x+self.button_size)/2
        self.button_y1=0
        self.button_y2=self.button_size


    def DrawPermanentObjects(self):
        for entr in self.instance.desirable_dict:
            pygame.draw.circle(self.screen, green, self.instance.desirable_dict[entr], 3, 2)
        for entr in self.instance.obnoxious_dict:
            pygame.draw.circle(self.screen, red, self.instance.obnoxious_dict[entr], 3, 2)
        pygame.draw.rect(self.screen, blue, (self.button_x1, self.button_y1, 50, 50), 2)
# desirable_dict,obnoxious_dict={1:[70,60],2:[20,400],3:[260,540],4:[700,505],5:[209,60],6:[700,465],7:[70,40]},{8:[140,20],9:[490,780]}

    def EventRoutine(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.ButtonClicked(event,self.button_x1,self.button_x2,self.button_y1,self.button_y2)


    def ShowUp(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.max_x, self.max_y))
        pygame.display.set_caption("Facility Location")
        self.screen.fill(black)

        self.DrawPermanentObjects()

        pygame.display.flip()
        self.sol_points = []
        on = True
        while not self.done:
            self.clock.tick(100)

            self.EventRoutine()
            if self.sol_points!=[]:
                for point in self.sol_points:
                    if on == True:
                        pygame.draw.circle(self.screen, yellow, point, 3, 2)
                        pygame.display.flip()
                        on = False
                    else:
                        pygame.draw.circle(self.screen, black, point, 3, 2)
                        pygame.display.flip()
                        on = True
        pygame.quit()

    def Solve(self):
        var_sol_dict, objective = self.model_solver.SolveNewProblem()
        x, y = int(round(var_sol_dict["new_a"][()])), int(round(var_sol_dict["new_b"][()]))
        self.sol_points = [(x, y)]
        print(self.sol_points[0][0], self.sol_points[0][1])
        pygame.draw.circle(self.screen, yellow, self.sol_points[0], 5, 2)
        pygame.display.flip()
    def Create(self):
        pass
    def Draw(self):
        pass

    def ButtonClicked(self, event, button_x1,button_x2,button_y1,button_y2):
        if button_x1 <= event.pos[0] <= button_x2 and button_y1 <= event.pos[1] <= button_y2:
            return True
        else:
            return False