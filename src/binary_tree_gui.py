import pygame
import sys
from pathlib import Path

# Handle import error
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.Program3_binary_tree import BinaryTree, Traversal
from src.constants import *

class Button:
    # Simple button class for mouse click detection.
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.is_hovered = False
    
    def draw(self, screen, font):
        # Draw button
        color = tuple(min(c + 30, 255) for c in self.color) if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)
        
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, pos):
        # Check if button is clicked
        return self.rect.collidepoint(pos)
    
    def update_hover(self, pos):
        # Check if button is hovered
        self.is_hovered = self.rect.collidepoint(pos)


class BinaryTreeGUI:

    def __init__(self):
         # Initialize pygame and the GUI components.
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 
                                            pygame.RESIZABLE
                                               | pygame.SCALED 
                                               | pygame.FULLSCREEN
                                               | pygame.SHOWN)
        pygame.display.set_caption("Binary Tree Visualizer")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 56)
        self.font_medium = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 28)
        self.font_traversal = pygame.font.Font(None, 28)
        
        self.bin_tree = None
        self.tree_level = 0
        self.node_positions = {}
        self.input_values = []
        self.current_input_index = 0
        self.current_input_text = ""
        self.stage = "level_input"
        
    def get_tree_level(self):
        # Display buttons to select the number of levels for the binary tree.

        buttons = []
        
        # Create level buttons
        for level in range(1, 6):
            x = 280 + (level - 1) * 150
            button = Button(x, 320, 120, 80, str(level), (100, 100, 100), (240, 240, 240))
            buttons.append((level, button))
        
        while self.stage == "level_input":
            mouse_pos = pygame.mouse.get_pos()
            
            self.screen.fill(COLOR_BACKGROUND)
            
            title = self.font_large.render("Binary Tree Visualizer", True, COLOR_TEXT)
            prompt = self.font_medium.render("Select number of levels (1-5):", True, COLOR_TEXT)
            
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
            self.screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 200))
            
            # Update and draw buttons
            for level, button in buttons:
                button.update_hover(mouse_pos)
                button.draw(self.screen, self.font_medium)
            
            pygame.display.flip()
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for level, button in buttons:
                        if button.is_clicked(mouse_pos):
                            self.stage = "tree_display"
                            return level
    
    def calculate_node_positions(self):
        # Calculate the positions of all nodes for rendering.
        if not self.bin_tree:
            return
        
        self.node_positions = {}
        
        # Recursive function to calculate positions based on subtree width
        def position_node(index, x, y, spacing):
            if index >= len(self.bin_tree.all_nodes):
                return
            
            # Store position for this node
            self.node_positions[index] = (x, y)
            
            # Calculate children indices
            left_index = 2 * index + 1
            right_index = 2 * index + 2
            
            # Reduce spacing for next level
            next_spacing = spacing // 2
            next_y = y + 140
            
            # Position left child
            if left_index < len(self.bin_tree.all_nodes):
                position_node(left_index, x - spacing, next_y, next_spacing)
            
            # Position right child
            if right_index < len(self.bin_tree.all_nodes):
                position_node(right_index, x + spacing, next_y, next_spacing)
        
        # Start positioning from root with initial spacing
        initial_spacing = SCREEN_WIDTH // 6
        position_node(0, SCREEN_WIDTH // 2, 50, initial_spacing)
    
    def draw_tree(self):
        # Draw the binary tree structure on the screen.
        if not self.bin_tree:
            return
        
        # Draw connectors first (so they appear behind nodes)
        for index, node in enumerate(self.bin_tree.all_nodes):
            if index not in self.node_positions:
                continue
            
            parent_pos = self.node_positions[index]
            
            # Draw to left child
            left_index = 2 * index + 1
            if left_index < len(self.bin_tree.all_nodes) and left_index in self.node_positions:
                child_pos = self.node_positions[left_index]
                pygame.draw.line(self.screen, COLOR_CONNECTOR, parent_pos, child_pos, 2)
            
            # Draw to right child
            right_index = 2 * index + 2
            if right_index < len(self.bin_tree.all_nodes) and right_index in self.node_positions:
                child_pos = self.node_positions[right_index]
                pygame.draw.line(self.screen, COLOR_CONNECTOR, parent_pos, child_pos, 2)
        
        # Draw nodes
        for index, node in enumerate(self.bin_tree.all_nodes):
            if index not in self.node_positions:
                continue
            
            x, y = self.node_positions[index]
            
            # Choose color based on node value
            if node.value is None:
                color = COLOR_NONE_NODE
            else:
                color = COLOR_NODE
            
            # Draw circle
            pygame.draw.circle(self.screen, color, (int(x), int(y)), NODE_RADIUS)
            pygame.draw.circle(self.screen, COLOR_NODE_BORDER, (int(x), int(y)), NODE_RADIUS, 2)
            
            # Draw value inside node
            if node.value is not None:
                value_text = self.font_medium.render(str(node.value), True, (0, 0, 0))
                self.screen.blit(value_text, (int(x) - value_text.get_width() // 2, 
                                              int(y) - value_text.get_height() // 2))
    
    def get_node_inputs(self):
        # Get user inputs for each node in the tree.
        self.input_values = [None] * len(self.bin_tree.all_nodes)
        self.current_input_index = 0
        self.current_input_text = ""
        
        while self.stage == "node_input":
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(COLOR_BACKGROUND)
            
            # Draw tree with placeholders
            self.draw_tree()
            
            # Draw input section at the bottom
            input_y = SCREEN_HEIGHT - 120
            
            # Title
            title = self.font_medium.render(f"Node {self.current_input_index + 1}/{len(self.bin_tree.all_nodes)}", 
                                           True, COLOR_TEXT)
            self.screen.blit(title, (50, input_y - 50))
            
            # Input label
            input_label = self.font_small.render("Enter value (or '.' for None):", True, (150, 150, 150))
            self.screen.blit(input_label, (50, input_y - 25))
            
            # Input box
            input_box_rect = pygame.Rect(50, input_y, 250, 40)
            pygame.draw.rect(self.screen, COLOR_INPUT_BG, input_box_rect)
            pygame.draw.rect(self.screen, COLOR_HIGHLIGHT, input_box_rect, 2)
            
            # Input text
            input_text_render = self.font_medium.render(self.current_input_text, True, COLOR_TEXT)
            self.screen.blit(input_text_render, (60, input_y + 8))
            
            # Buttons
            confirm_button = Button(320, input_y, 110, 40, "Confirm", (80, 120, 80), (240, 240, 240))
            backspace_button = Button(440, input_y, 110, 40, "Clear", (120, 80, 80), (240, 240, 240))
            none_button = Button(560, input_y, 110, 40, "None", (80, 80, 120), (240, 240, 240))
            restart_button = Button(680, input_y, 130, 40, "Restart", (120, 80, 80), (240, 240, 240))
            
            confirm_button.update_hover(mouse_pos)
            backspace_button.update_hover(mouse_pos)
            none_button.update_hover(mouse_pos)
            restart_button.update_hover(mouse_pos)
            
            confirm_button.draw(self.screen, self.font_small)
            backspace_button.draw(self.screen, self.font_small)
            none_button.draw(self.screen, self.font_small)
            restart_button.draw(self.screen, self.font_small)
            
            pygame.display.flip()
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if confirm_button.is_clicked(mouse_pos):
                        if self.current_input_text.strip() == "":
                            pass
                        else:
                            if self.current_input_text == ".":
                                self.input_values[self.current_input_index] = None
                            else:
                                self.input_values[self.current_input_index] = self.current_input_text
                            
                            if self.current_input_index < len(self.bin_tree.all_nodes) - 1:
                                self.current_input_index += 1
                                self.current_input_text = ""
                            else:
                                self.stage = "traversal_display"
                                return "continue"
                            
                    elif backspace_button.is_clicked(mouse_pos):
                        self.current_input_text = self.current_input_text[:-1]
                    elif none_button.is_clicked(mouse_pos):
                        self.input_values[self.current_input_index] = None
                        
                        if self.current_input_index < len(self.bin_tree.all_nodes) - 1:
                            self.current_input_index += 1
                            self.current_input_text = ""
                        else:
                            self.stage = "traversal_display"
                            return "continue"
                    elif restart_button.is_clicked(mouse_pos):
                        return "restart"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.current_input_text = self.current_input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        if self.current_input_text.strip() == "":
                            pass
                        else:
                            if self.current_input_text == ".":
                                self.input_values[self.current_input_index] = None
                            else:
                                self.input_values[self.current_input_index] = self.current_input_text
                            
                            if self.current_input_index < len(self.bin_tree.all_nodes) - 1:
                                self.current_input_index += 1
                                self.current_input_text = ""
                            else:
                                self.stage = "traversal_display"
                                return "continue"
                            
                    else:
                        if len(self.current_input_text) < 20:
                            self.current_input_text += event.unicode
    
    def apply_values_to_tree(self):
        # Apply the input values to the nodes
        for index, node in enumerate(self.bin_tree.all_nodes):
            if self.input_values[index] is None:
                node.value = None
            else:
                node.value = self.input_values[index]
    
    def remove_deleted_descendants(self):
        # Remove descendant nodes if their parent is Non
        for node in self.bin_tree.all_nodes:
            if node.value is None:
                # Mark all descendants as None
                self._mark_descendants_none(node)
    
    def _mark_descendants_none(self, node):
        # Recursively mark descendants of node as None
        if node is None:
            return
        
        if node.left_child:
            node.left_child.value = None
            self._mark_descendants_none(node.left_child)
        
        if node.right_child:
            node.right_child.value = None
            self._mark_descendants_none(node.right_child)
    
    def display_traversals(self):
        # Display the traversal results of the binary tree
        traversal = Traversal(self.bin_tree)
        preorder = traversal.preorder_traversal()
        inorder = traversal.inorder_traversal()
        postorder = traversal.postorder_traversal()
        
        while self.stage == "traversal_display":
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(COLOR_BACKGROUND)
            
            # Draw tree
            self.draw_tree()
            
            # Draw traversals at the bottom
            traversal_y = SCREEN_HEIGHT - 140
            
            preorder_text = self.font_traversal.render(f"Preorder (TLR): {preorder}", True, COLOR_TEXT)
            inorder_text = self.font_traversal.render(f"Inorder (LTR): {inorder}", True, COLOR_TEXT)
            postorder_text = self.font_traversal.render(f"Postorder (LRT): {postorder}", True, COLOR_TEXT)
            
            self.screen.blit(preorder_text, (50, traversal_y))
            self.screen.blit(inorder_text, (50, traversal_y + 30))
            self.screen.blit(postorder_text, (50, traversal_y + 60))
            
            # Buttons
            exit_button = Button(SCREEN_WIDTH - 310, traversal_y + 80, 100, 40, "Exit", (120, 80, 80), (240, 240, 240))
            restart_button = Button(SCREEN_WIDTH - 190, traversal_y + 80, 130, 40, "Restart", (80, 120, 80), (240, 240, 240))
            
            exit_button.update_hover(mouse_pos)
            restart_button.update_hover(mouse_pos)
            
            exit_button.draw(self.screen, self.font_small)
            restart_button.draw(self.screen, self.font_small)
            
            pygame.display.flip()
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button.is_clicked(mouse_pos):
                        return "exit"
                    elif restart_button.is_clicked(mouse_pos):
                        return "restart"
    
    def run(self):
        # Sub encapsulation for program
        while True:
            # Stage 1: Get tree level
            self.stage = "level_input"
            self.tree_level = self.get_tree_level()
            
            # Stage 2: Create and display tree
            self.bin_tree = BinaryTree(self.tree_level)
            self.bin_tree.build_tree()
            self.calculate_node_positions()
            self.stage = "node_input"
            
            # Stage 3: Get node inputs
            input_result = self.get_node_inputs()
            
            if input_result == "restart":
                continue
            
            # Apply values and process tree
            self.apply_values_to_tree()
            self.remove_deleted_descendants()
            
            # Stage 4: Display traversals
            result = self.display_traversals()
            
            # If result == "restart", loop continues
            if result == "exit":
                pygame.quit()
                break


def main():
    # Encapsulation for main.py
    gui = BinaryTreeGUI()
    gui.run()


if __name__ == "__main__":
    main()
