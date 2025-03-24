class Item:
    def __init__(self, id: int, name: str, description: str, price: float):
        self.id = id
        self.name = name
        self.description = description
        self.price = price

    def __setattr__(self, name, value):
        if name == 'id':
            if not isinstance(value, int) or value <= 0:
                raise ValueError("ID must be a positive integer")
        elif name == 'name':
            if not isinstance(value, str) or not value.strip():
                raise ValueError("Name must be a non-empty string")
        elif name == 'description':
            if not isinstance(value, str):
                raise ValueError("Description must be a string")
        elif name == 'price':
            if not isinstance(value, (int, float)) or value <= 0:
                raise ValueError("Price must be a positive number")
            value = round(float(value), 2)
        
        if name in ['name', 'description']:
            value = value.strip()
            
        super().__setattr__('_' + name, value)

    def __getattr__(self, name):
        if name in ['id', 'name', 'description', 'price']:
            return super().__getattribute__('_' + name)
        raise AttributeError(f"'Item' object has no attribute '{name}'")

    def __str__(self):
        return f"Item(ID: {self.id}, Name: '{self.name}', Price: ${self.price:.2f}, Description: '{self.description}')"


class ItemManager:
    def __init__(self):
        self.items = {}
        self.next_id = 1

    def create_item(self, name: str, description: str, price: float) -> Item:
        try:
            item = Item(self.next_id, name, description, price)
            self.items[item.id] = item
            self.next_id += 1
            return item
        except ValueError as e:
            raise ValueError(f"Failed to create item: {str(e)}")

    def read_item(self, item_id: int) -> Item:
        if not isinstance(item_id, int) or item_id <= 0:
            raise ValueError("Invalid item ID")
        if item_id not in self.items:
            raise ValueError(f"Item with ID {item_id} not found")
        return self.items[item_id]

    def read_all_items(self) -> list:
        return list(self.items.values())

    def update_item(self, item_id: int, name: str = None, description: str = None, price: float = None) -> Item:
        item = self.read_item(item_id)
        if name is not None:
            item.name = name
        if description is not None:
            item.description = description
        if price is not None:
            item.price = price
        return item

    def delete_item(self, item_id: int) -> bool:
        if not isinstance(item_id, int) or item_id <= 0:
            raise ValueError("Invalid item ID")
        if item_id in self.items:
            del self.items[item_id]
            return True
        return False


def display_menu():
    print("\nItem Management System")
    for i, option in enumerate([
        "Create a new item",
        "List all items",
        "View item details",
        "Update an item",
        "Delete an item",
        "Exit"
    ], 1):
        print(f"{i}. {option}")


def get_input(prompt, type_func=str, validation_func=None):
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                raise ValueError("Input cannot be empty")
            converted = type_func(value)
            if validation_func and not validation_func(converted):
                raise ValueError("Invalid input")
            return converted
        except ValueError as e:
            print(f"Error: {str(e)}. Please try again.")


def main():
    manager = ItemManager()
    while True:
        display_menu()
        try:
            choice = get_input("Enter your choice (1-6): ", int, lambda x: 1 <= x <= 6)
            
            if choice == 1:
                print("\nCreate a new item")
                item = manager.create_item(
                    get_input("Enter item name: "),
                    get_input("Enter item description: "),
                    get_input("Enter item price: ", float, lambda x: x > 0)
                )
                print(f"Item created successfully: {item}")
                
            elif choice == 2:
                print("\nAll Items:")
                items = manager.read_all_items()
                if items:
                    for item in items:
                        print(item)
                else:
                    print("No items found.")
                    
            elif choice == 3:
                item_id = get_input("Enter item ID to view: ", int, lambda x: x > 0)
                try:
                    item = manager.read_item(item_id)
                    print("\nItem Details:")
                    print(f"ID: {item.id}")
                    print(f"Name: {item.name}")
                    print(f"Description: {item.description}")
                    print(f"Price: ${item.price:.2f}")
                except ValueError as e:
                    print(f"Error: {str(e)}")
                    
            elif choice == 4:
                item_id = get_input("Enter item ID to update: ", int, lambda x: x > 0)
                try:
                    print("\nLeave field blank to keep current value")
                    current = manager.read_item(item_id)
                    
                    name = input(f"Enter new name [{current.name}]: ").strip()
                    description = input(f"Enter new description [{current.description}]: ").strip()
                    price = input(f"Enter new price [${current.price:.2f}]: ").strip()
                    
                    item = manager.update_item(
                        item_id,
                        name=name if name else None,
                        description=description if description else None,
                        price=float(price) if price else None
                    )
                    print(f"Item updated successfully: {item}")
                except ValueError as e:
                    print(f"Error: {str(e)}")
                    
            elif choice == 5:
                item_id = get_input("Enter item ID to delete: ", int, lambda x: x > 0)
                try:
                    if manager.delete_item(item_id):
                        print("Item deleted successfully")
                    else:
                        print("Item not found")
                except ValueError as e:
                    print(f"Error: {str(e)}")
                    
            elif choice == 6:
                print("Exiting the application. Goodbye!")
                break
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()