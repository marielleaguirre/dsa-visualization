import pygame                 # Graphics and UI
import sys                    # Exit program
import os                     # File path handling
from datetime import datetime # Time stamps

pygame.init()                 # Initialize pygame

# ==================== WINDOW ====================
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Stack Parking Garage Simulation")

CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas", 18)
SMALL_FONT = pygame.font.SysFont("consolas", 12)
BIG_FONT = pygame.font.SysFont("consolas", 26)

# ==================== COLORS ====================
BG = (25, 25, 25)
GARAGE = (200, 200, 200)
CAR_COLOR = (70, 160, 255)
BTN = (90, 90, 90)
BTN_HOVER = (130, 130, 130)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 60, 60)
GREEN = (60, 200, 120)
INPUT_BG = (255, 255, 255)
INPUT_ACTIVE = (200, 230, 255)

# ==================== GARAGE SETTINGS ====================
CAPACITY = 5
SLOT_W = 220          # Slot width
SLOT_H = 70           # Slot height
STACK_X = 550         # X position of vertical stack
BOTTOM_Y = 520        # Bottom slot position (first car)

# ==================== MESSAGE SYSTEM ====================
message_text = ""
message_color = GREEN
message_time = 0

def show_message(text, color=GREEN):
    global message_text, message_color, message_time
    message_text = text
    message_color = color
    message_time = pygame.time.get_ticks()

def draw_message():
    if message_text and pygame.time.get_ticks() - message_time < 2000:
        pygame.draw.rect(screen, message_color, (250, 10, 500, 40), border_radius=8)
        msg = FONT.render(message_text, True, BLACK)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 22))

# ==================== CAR CLASS ====================
class Car:
    """Represents a single car"""

    def __init__(self, plate):
        self.plate = plate
        self.time_in = datetime.now().strftime("%H:%M:%S")
        self.time_out = None

        # Load car image
        try:
            car_image_path = os.path.join(os.path.dirname(__file__), "car.png")
            car_image_path = os.path.abspath(car_image_path)
            original_image = pygame.image.load(car_image_path)
            # Scale image narrower (50% width, 70% height)
            self.image = pygame.transform.scale(original_image, (int((SLOT_W - 20) * 0.5), int((SLOT_H - 10) * 0.7)))
        except Exception as e:
            self.image = None  # Fallback if image not found

        # Start from top right on-screen, moving in horizontally then falling
        self.x = WIDTH - 100       # Start on-screen right
        self.y = 50                # Start near top
        self.target_x = STACK_X + 12  # Align with stack
        self.target_y = BOTTOM_Y   # Will be updated by update_targets()

    def move(self):
        # Move horizontally first (from right to parking spot)
        if self.x > self.target_x:
            self.x -= 8
            return

        # Then move vertically down into the slot
        if self.y < self.target_y:
            self.y += 8

    def draw(self):
        if self.image:
            # Center the smaller image in the slot
            img_x = self.x + (SLOT_W - 20 - self.image.get_width()) // 2
            img_y = self.y + (SLOT_H - 10 - self.image.get_height()) // 2
            screen.blit(self.image, (img_x, img_y))
            
            # Plate number above the car, centered, inside the slot
            plate_text = SMALL_FONT.render(self.plate, True, BLACK)
            plate_x = self.x + (SLOT_W - 20 - plate_text.get_width()) // 2
            screen.blit(plate_text, (plate_x, self.y + 3))
            
            # Time below the car, centered, inside the slot
            time_text = SMALL_FONT.render(self.time_in, True, BLACK)
            time_x = self.x + (SLOT_W - 20 - time_text.get_width()) // 2
            screen.blit(time_text, (time_x, self.y + SLOT_H - 22))
        else:
            pygame.draw.rect(
                screen, CAR_COLOR,
                (self.x, self.y, SLOT_W - 20, SLOT_H - 10),
                border_radius=10
            )
            # Plate and time centered on the rectangle
            plate_text = SMALL_FONT.render(self.plate, True, BLACK)
            plate_x = self.x + (SLOT_W - 20 - plate_text.get_width()) // 2
            screen.blit(plate_text, (plate_x, self.y + 8))
            
            time_text = SMALL_FONT.render(self.time_in, True, BLACK)
            time_x = self.x + (SLOT_W - 20 - time_text.get_width()) // 2
            screen.blit(time_text, (time_x, self.y + 28))

# ==================== STACK GARAGE ====================
class ParkingGarage:
    """
    STACK (LIFO):
    - PUSH → car placed on TOP
    - POP  → top car removed first
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.stack = []      # Stack implemented using list
        self.departed = []

    def park(self, plate):
        """Push car onto stack"""
        if not plate:
            show_message("ERROR: Plate required!", RED)
            return

        if len(self.stack) >= self.capacity:
            show_message("ERROR: Stack is FULL!", RED)
            return

        for car in self.stack:
            if car.plate == plate:
                show_message("ERROR: Duplicate plate!", RED)
                return

        car = Car(plate)
        self.stack.append(car)     # PUSH
        self.update_targets()
        show_message(f"Car {plate} PUSHED to stack", GREEN)

    def depart(self):
        """Pop top car from stack"""
        if not self.stack:
            show_message("ERROR: Stack empty!", RED)
            return

        car = self.stack.pop()     # POP (LIFO)
        car.time_out = datetime.now().strftime("%H:%M:%S")
        self.departed.append(car)
        self.update_targets()
        show_message(f"Car {car.plate} POPPED from stack", GREEN)

    def update_targets(self):
        """Update target positions for all cars in stack"""
        for i, car in enumerate(self.stack):
            car.target_y = BOTTOM_Y - i * SLOT_H + 5 - SLOT_H

    def update(self):
        for car in self.stack:
            car.move()

# ==================== INPUT BOX ====================
class InputBox:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 10:
                    self.text += event.unicode.upper()

    def draw(self):
        color = INPUT_ACTIVE if self.active else INPUT_BG
        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=6)
        txt = FONT.render(self.text or "Enter Plate", True, BLACK)
        screen.blit(txt, (self.rect.x + 10, self.rect.y + 8))

    def clear(self):
        self.text = ""

# ==================== BUTTON ====================
class Button:
    def __init__(self, x, y, w, h, text, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action

    def draw(self):
        color = BTN_HOVER if self.rect.collidepoint(pygame.mouse.get_pos()) else BTN
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        screen.blit(FONT.render(self.text, True, BLACK),
                    (self.rect.x + 15, self.rect.y + 10))

    def click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.action()

# ==================== RECORDS SCREEN ====================
def draw_records(garage):
    screen.fill(BG)
    screen.blit(BIG_FONT.render("PARKING GARAGE RECORDS", True, WHITE), (330, 60))

    headers = ["PLATE", "TIME IN", "TIME OUT", "STATUS"]
    xs = [200, 360, 520, 690]

    for h, x in zip(headers, xs):
        screen.blit(FONT.render(h, True, WHITE), (x, 110))

    y = 150
    for car in garage.departed:
        screen.blit(FONT.render(car.plate, True, WHITE), (200, y))
        screen.blit(FONT.render(car.time_in, True, WHITE), (360, y))
        screen.blit(FONT.render(car.time_out, True, WHITE), (520, y))
        screen.blit(FONT.render("DEPARTED", True, WHITE), (690, y))
        y += 28

    for i, car in enumerate(reversed(garage.stack), start=1):
        screen.blit(FONT.render(car.plate, True, WHITE), (200, y))
        screen.blit(FONT.render(car.time_in, True, WHITE), (360, y))
        screen.blit(FONT.render("--", True, WHITE), (520, y))
        screen.blit(FONT.render(f"IN STACK (LEVEL {i})", True, WHITE), (690, y))
        y += 28

# ==================== MAIN ====================
garage = ParkingGarage(CAPACITY)
input_box = InputBox(40, 150, 200, 36)
screen_state = "garage"

def go_records():
    global screen_state
    screen_state = "records"

def go_garage():
    global screen_state
    screen_state = "garage"

buttons = [
    Button(40, 200, 170, 40, "PARK", lambda: (garage.park(input_box.text), input_box.clear())),
    Button(40, 250, 170, 40, "DEPART", garage.depart),
    Button(40, 300, 170, 40, "RECORDS", go_records),
    Button(40, 350, 170, 40, "EXIT", sys.exit),
]

back_button = Button(40, 560, 140, 40, "BACK", go_garage)

# ==================== MAIN LOOP ====================
running = True
while running:
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        input_box.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if screen_state == "garage":
                for b in buttons:
                    b.click()
            else:
                back_button.click()

    if screen_state == "garage":
        screen.blit(FONT.render("Plate Number:", True, WHITE), (40, 125))
        input_box.draw()

        screen.blit(FONT.render(f"PARKING GARAGE CAPACITY: {len(garage.stack)} / {CAPACITY}", True, WHITE), (40, 70))

        for b in buttons:
            b.draw()

        # Draw vertical garage shaft
        pygame.draw.rect(
            screen, GARAGE,
            (STACK_X, BOTTOM_Y - SLOT_H * CAPACITY - 20,
             SLOT_W, SLOT_H * CAPACITY + 20),
            border_radius=12
        )

        screen.blit(BIG_FONT.render("PARKING GARAGE", True, WHITE),
                    (STACK_X + 10, BOTTOM_Y - SLOT_H * CAPACITY - 55))

        # Draw stack slots
        for i in range(CAPACITY):
            pygame.draw.rect(
                screen, (100, 100, 100),
                (STACK_X + 10,
                 BOTTOM_Y - i * SLOT_H + 5 - SLOT_H,
                 SLOT_W - 20,
                 SLOT_H - 10),
                2
            )

        garage.update()
        for car in garage.stack:
            car.draw()

    else:
        draw_records(garage)
        back_button.draw()

    draw_message()
    pygame.display.flip()
    CLOCK.tick(60)

pygame.quit()

if __name__ == "__main__":
    pass  # The main loop runs automatically when the script is executed