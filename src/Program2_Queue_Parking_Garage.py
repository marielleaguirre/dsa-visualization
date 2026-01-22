import pygame                      # For graphics
import sys                         # For exiting program
from collections import deque      # Initialize the queue
from  datetime import datetime     # For timestamping

def main():
    pygame.init()                      # Initialize pygame

    # -------------------- WINDOW --------------------
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # FULL SCREEN MODE
    WIDTH, HEIGHT = screen.get_size()                            # Get actual screen size
    pygame.display.set_caption("Queue Parking Garage")           # Set window title

    CLOCK = pygame.time.Clock()                        # For controlling frame rate
    FONT = pygame.font.SysFont("consolas", 18)         # Set font for
    BIG_FONT = pygame.font.SysFont("consolas", 26, bold= True)     # Set big font for titles

    # -------------------- COLORS --------------------
    BG = (25, 25, 25)                 # Background color (very dark gray)
    GARAGE = (200, 200, 200)          # Garage color (light gray)
    CAR_COLOR = (70, 160, 255)        # Car color (blue)
    BTN = (90, 90, 90)                # Button color (dark gray)
    BTN_HOVER = (130, 130, 130)       # Button hover color (medium gray)
    WHITE = (255, 255, 255)           # White color
    BLACK = (0, 0, 0)                 # Black color
    RED = (220, 60, 60)               # Red color
    GREEN = (60, 200, 120)            # Green color
    INPUT_BG = (255, 255, 255)        # Input box background color (white)
    INPUT_ACTIVE = (200, 230, 255)    # Input box active color (light blue)

    # -------------------- GARAGE SETTINGS --------------------
    CAPACITY = 10                                # Maximum number of cars in garage
    SLOT_W = 130                                 # Width of each parking slot
    SLOT_H = 70                                  # Height of each parking slot
    START_X = (WIDTH - SLOT_W * CAPACITY) // 2   # Center garage horizontally
    START_Y = HEIGHT // 2 + 40                   # Center garage vertically

    # -------------------- LOAD IMAGES --------------------
    try:
        CAR_IMG = pygame.image.load("src/assets/car.png").convert_alpha()
        CAR_IMG = pygame.transform.scale(CAR_IMG, (SLOT_W - 20, SLOT_H - 10))
    except pygame.error:
        CAR_IMG = None  # fallback to drawing the blue rectangle

    # -------------------- MESSAGE SYSTEM --------------------
    message_text = ""                  # Message text to display
    message_color = GREEN              # Message color
    message_time = 0                   # Time when message was set

    def show_message(text, color=GREEN):                     # Function to show messages
        global message_text, message_color, message_time
        message_text = text                                  # Set the message text
        message_color = color                                # Set the message color
        message_time = pygame.time.get_ticks()               # Record the time the message was set

    def draw_message():                                                                     # Function to draw messages
        if message_text and pygame.time.get_ticks() - message_time < 2000:                  # Show message for 2 seconds
            pygame.draw.rect(screen, message_color, (WIDTH//2 - 250, 10, 500, 40), border_radius=8)
            msg = FONT.render(message_text, True, BLACK)                                    # Render the message text
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 22))                       # Center the message text

    # -------------------- DATA CLASSES --------------------
    class Car:                                                       # Created a blueprint for Car
        def __init__(self, plate_num):                               
            self.plate_num = plate_num                               # Stores car's plate number
            self.time_in = datetime.now().strftime("%H:%M:%S")       # Records current time as time in with format HH:MM:SS
            self.time_out = None
            self.x = WIDTH
            self.y = START_Y + 5
            self.target_x = 0                    # Setting car's starting position

        def move(self):                          # Function to move the car towards target position
            if self.x > self.target_x:
                self.x -= 8

        def draw(self):  # Function to draw the car on the screen
            if CAR_IMG:     # Check if a car image has been successfully loaded
                screen.blit(CAR_IMG, (self.x, self.y))      # Draw the car image
            else:
                pygame.draw.rect(screen, CAR_COLOR, (self.x, self.y, SLOT_W-20, SLOT_H-10))    # Draw a rectangle if no image is available
            # Optional: keep plate number and time text
            # Render texts
            plate_txt = FONT.render(self.plate_num, True, BLACK)
            time_txt = FONT.render(self.time_in, True, BLACK)

            # Center plate number horizontally, near top of car
            plate_x = self.x + (SLOT_W - plate_txt.get_width()) // 2
            plate_y = self.y + -3  # small offset from top
            screen.blit(plate_txt, (plate_x, plate_y))

            # Center time horizontally, near bottom of car
            time_x = self.x + (SLOT_W - time_txt.get_width()) // 2
            time_y = self.y + SLOT_H - time_txt.get_height() - 5  # small offset from bottom
            screen.blit(time_txt, (time_x, time_y))

    class ParkingGarage:                              # Created a blueprint for Parking Garage
        def __init__(self, capacity):
            self.capacity = capacity                  # Set garage capacity            
            self.queue = deque()                      # Initializes an empty queue to store parked cars
            self.departed = []                        # List to store departed cars
        
        def park(self, plate_num):                   # Function to park a car
            if not plate_num:                        # Check if plate number is empty
                show_message("ERROR: Plate number cannot be empty!", RED)
                return
            
            if len(self.queue) >= CAPACITY:          # Check if garage is full
                show_message("ERROR: Garage is FULL! Car cannot enter.", RED)
                return
            
            for car in self.queue:                   # Check for duplicate plate numbers
                if car.plate_num == plate_num:
                    show_message(f"ERROR: Plate '{plate_num}' is already parked!", RED)
                    return

            car = Car(plate_num)                     # Create a new car instance
            self.queue.append(car)                   # Add the car to the queue
            self.update_targets()                    # Update target positions of all cars
            show_message(f"SUCCESS: Car {plate_num} parked!", GREEN)  # Show success message

        def depart(self):                              # Function to remove a car
            if not self.queue:                         # Check if there are any cars parked
                show_message("No cars to remove.", RED)
                return

            car = self.queue.popleft()                             # Remove the first car in the queue
            car.time_out = datetime.now().strftime("%H:%M:%S")     # Record the time out
            self.departed.append(car)                              # Add the car to the departed list
            self.update_targets()                                  # Update target positions of remaining cars
            show_message(f"SUCCESS: Car {car.plate_num} departed!", GREEN)

        def update_targets(self):                   # Function to update target positions of cars
            for i, car in enumerate(self.queue):
                car.target_x = START_X + i * SLOT_W + 10
                car.y = START_Y + 5

        def update(self):                           # Function to update car positions
            for car in self.queue:
                car.move()
        
    # -------------------- INPUT BOX --------------------
    class InputBox:                                 # Class for input box
        def __init__(self, x, y, w, h):             # Initialize input box
            self.rect = pygame.Rect(x, y, w, h)     # Define rectangle for input box
            self.text = ""                  # Initialize text as empty
            self.active = False             # Input box is not active initially

        def handle_event(self, event):            # Function to handle events
            if event.type == pygame.MOUSEBUTTONDOWN:             # Check for mouse click
                self.active = self.rect.collidepoint(event.pos)  # Toggle active state if clicked
                
            if event.type == pygame.KEYDOWN and self.active:     # Check for key press when active
                if event.key == pygame.K_BACKSPACE:              # Handle backspace
                    self.text = self.text[:-1]
                else:                                           # Add character to text
                    if len(self.text) < 10:                     # Limit input length
                        self.text += event.unicode.upper()      # Convert to uppercase

        def draw(self):                                                         # Function to draw input box
            color = INPUT_ACTIVE if self.active else INPUT_BG                   # Change color if active
            pygame.draw.rect(screen, color, self.rect, border_radius=6)         # Draw input box
            pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=6)      # Draw border
            txt = FONT.render(self.text or "Enter Plate Number", True, BLACK)   # Render the text
            screen.blit(txt, (self.rect.x + 10, self.rect.y + 8))               # Blit text onto input box

        def clear(self):          # Function to clear input box
            self.text = ""

    # -------------------- BUTTON --------------------
    class Button:                                       # Class for button
        def __init__(self, x, y, w, h, text, action):   # Initialize button
            self.rect = pygame.Rect(x, y, w, h)         # Define rectangle for button
            self.text = text                            # Button text
            self.action = action                        # Action to perform on click

        def draw(self):             # Function to draw button
            color = BTN_HOVER if self.rect.collidepoint(pygame.mouse.get_pos()) else BTN  # Change color on hover
            pygame.draw.rect(screen, color, self.rect, border_radius=8)  # Draw button
            txt = FONT.render(self.text, True, BLACK)  # Render text
            # Center text in the button rectangle
            text_x = self.rect.x + (self.rect.width - txt.get_width()) // 2
            text_y = self.rect.y + (self.rect.height - txt.get_height()) // 2
            screen.blit(txt, (text_x, text_y))

        def click(self):             # Function to handle button click
            if self.rect.collidepoint(pygame.mouse.get_pos()):    # Check if button is clicked
                self.action()

    # -------------------- RECORDS SCREEN --------------------
    def draw_records(garage):                     # Display parking records
        screen.fill(BG)
        screen.blit(BIG_FONT.render("PARKING RECORDS", True, WHITE), (WIDTH // 2 - 150, 60))
        
        headers = ["PLATE NUMBER", "TIME IN", "TIME OUT", "STATUS"]
        x_positions = [
            WIDTH//2 - 300,
            WIDTH//2 - 100,
            WIDTH//2 + 80,
            WIDTH//2 + 260
        ]

        for h, x in zip(headers, x_positions):   # Draw headers
            screen.blit(FONT.render(h, True, WHITE), (x, 110))

        y = 150
        for car in garage.departed:              # Draw departed cars
            screen.blit(FONT.render(car.plate_num, True, WHITE), (x_positions[0], y))
            screen.blit(FONT.render(car.time_in, True, WHITE), (x_positions[1], y))
            screen.blit(FONT.render(car.time_out, True, WHITE), (x_positions[2], y))
            screen.blit(FONT.render("DEPARTED", True, WHITE), (x_positions[3], y))
            y += 28
        
        for i, car in enumerate(garage.queue, start=1):  # Draw parked cars
            screen.blit(FONT.render(car.plate_num, True, WHITE), (x_positions[0], y))
            screen.blit(FONT.render(car.time_in, True, WHITE), (x_positions[1], y))
            screen.blit(FONT.render("--", True, WHITE), (x_positions[2], y))
            screen.blit(FONT.render(f"PARKED (Slot {i})", True, WHITE), (x_positions[3], y))
            y += 28

    # -------------------- MAIN --------------------
    garage = ParkingGarage(capacity = 5)                  # Create parking garage instance
    input_box = InputBox(40, 150, 200, 36)    # Create input box instance
    screen_state = "garage"                   # Set initial screen state

    def go_records():                # Function to switch to records screen
        global screen_state
        screen_state = "records"

    def go_garage():                 # Function to switch to garage screen
        global screen_state
        screen_state = "garage"

    buttons = [                     # Create buttons
        Button(40, 200, 170, 40, "PARK", lambda: (garage.park(input_box.text), input_box.clear())),
        Button(40, 250, 170, 40, "DEPART", garage.depart),
        Button(40, 300, 170, 40, "RECORDS", go_records),
        Button(40, 350, 170, 40, "EXIT", sys.exit),
    ]

    back_button = Button(40, HEIGHT - 100, 140, 40, "BACK", go_garage)  # Back button for records screen

    # -------------------- MAIN LOOP --------------------
    running = True
    while running:
        screen.fill(BG)                     # Fill background

        for event in pygame.event.get():    # Event handling
            if event.type == pygame.QUIT:   # Check for quit event
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False     # Exit on ESC key

            input_box.handle_event(event)   # Handle input box events

            if event.type == pygame.MOUSEBUTTONDOWN:  # Handle button clicks
                if screen_state == "garage":
                    for button in buttons:
                        button.click()
                else:
                    back_button.click()

        if screen_state == "garage":        # Garage screen
            screen.blit(FONT.render("Plate Number:", True, WHITE), (40, 125))  # Draw label
            input_box.draw()

            screen.blit(FONT.render(f"Parked Cars: {len(garage.queue)} / {CAPACITY}", True, WHITE), (40, 70))  # Draw parked cars count
            screen.blit(FONT.render(f"Departed Cars: {len(garage.departed)}", True, WHITE), (40, 95))  # Draw departed cars count

            for button in buttons:          # Draw buttons
                button.draw()

            pygame.draw.rect(
                screen, GARAGE,
                (START_X - 30, START_Y - 60,
                SLOT_W * CAPACITY + 60, SLOT_H + 120),
                border_radius=12
            )                       # Draw garage outline

            title_text = BIG_FONT.render("PARKING GARAGE (FIFO QUEUE)", True, BLACK)
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, START_Y - 50))  # Draw garage title

            for i in range(CAPACITY):   
                pygame.draw.rect(
                    screen, (100, 100, 100),
                    (START_X + i * SLOT_W, START_Y, SLOT_W - 10, SLOT_H), 2
                )               # Draw parking slots

            garage.update()              # Update car positions
            for car in garage.queue:     # Draw parked cars
                car.draw()

        else:                            # Records screen
            draw_records(garage)         # Draw parking records
            back_button.draw()           # Draw back button

        draw_message()                  # Draw any messages
        pygame.display.flip()           # Update the display
        CLOCK.tick(60)                  # Maintain 60 FPS

    pygame.quit()                       # Quit pygame

if __name__ == "__main__":
    main()