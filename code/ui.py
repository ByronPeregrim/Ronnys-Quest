import pygame

class UI:
    def __init__(self,surface):
        
        # setup
        self.display_surface = surface
        self.font = pygame.font.Font('../graphics/ui/ARCADEPI.TTF',30)

        # health
        self.health_bar = pygame.image.load('../graphics/ui/health.png').convert_alpha()
        self.health_bar = pygame.transform.scale(self.health_bar,(50,50))
        self.health_bar_rect = self.health_bar.get_rect(topleft = (20,10))

        # coins
        self.coin = pygame.image.load('../graphics/ui/coin.png').convert_alpha()
        self.coin = pygame.transform.scale(self.coin,(50,50))
        self.coin_rect = self.coin.get_rect(topleft = (50,61))
        

    def show_health(self,current,full):
        self.display_surface.blit(self.health_bar,self.health_bar_rect)
        health_amount_surf = self.font.render(str(current) + '%',False,'gray')
        health_amount_rect = health_amount_surf.get_rect(midleft = (self.health_bar_rect.right + 4,self.health_bar_rect.centery + 3))
        self.display_surface.blit(health_amount_surf,health_amount_rect)

    def show_coins(self,amount):
        self.display_surface.blit(self.coin,self.coin_rect)
        coin_amount_surf = self.font.render(str(amount),False,'gray')
        coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 4,self.coin_rect.centery + 3))
        self.display_surface.blit(coin_amount_surf,coin_amount_rect)