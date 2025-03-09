class Node:
    def __init__(self, data = None):
        self.data = data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def iter(self):
        current = self.head
        while current:
            value = current.data
            current = current.next
            yield value 

    def append(self, data):
        # Create a node with the data
        node = Node(data)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node

    def append_with_tail(self, data):
        node = Node(data)
        if self.tail:
            self.tail.next = node
        else:
            self.head = node
            self.tail = node

    def appen_at_a_location(self, data, index):
        current = self.head
        previous = self.head
        node = Node(data)
        count = 1

        while current:
            if count == 1:
                node.next = current
                self.head = node
                print(count)
                return
            elif index == index:
                node.next = current
                previous.next = node
                return 
            count += 1
            previous = current
            current = current.next
        if count < index:
            print("The list has fewer number of elements")

    def search(self,data):
        for node in self.iter():
            if data == node:
                return True
        return False

    def size(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def delete_first_node (self):
        current = self.head
        if self.head is None:
            print("No data element to delete")
        elif current == self.head:
            self.head = current.next

    def delete_last_element (self):
        current = self.head
        previous = self.head

        while current:
            if current.next is None:
                previous.next = current.next
                self.size -= 1
            previous = current
            current = current.next

    def delete(self, data):
        current = self.head
        previous = self.head
        while current:
            if current.data == data:
                if current == self.head:
                    self.head = current.next
                else:
                    previous.next = current.next
                self.size -= 1
                return
            previous = current
            current = current.next

            