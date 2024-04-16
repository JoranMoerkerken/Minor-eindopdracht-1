#!/usr/bin/env python3
"""Linked List -> Extended Linked List Implementation: Homework

The goal of this homework is to implement a singly linked list data structure with additional functionalities. 
In previous tutorials you have learned how a node and a linked list data structure in its basic form can be created.
However, a LinkedList class can have more methods to perform additional operations on a linked list,
such as: insertion (begin, end, or after a specific element), deletion, traversal, and sorting.

Your task is to:
    * locate the TODOs in this file
    * complete the missing part from the code 
    * run the test of this homework located in same folder.

To test run LinkedList_t.py in your command line'

Notes:
    * do not change class structure or method signature to not break unit tests
    * visit this url for more information on linked list:
    https://realpython.com/linked-lists-python/
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    #TODO 1: Insert at the beginning of the list
    def insertBeg(self, new_data):
        new_node = Node(new_data)
        new_node.next = self.head
        self.head = new_node
    
    #TODO 2: Insert at the end
    def insertEnd(self, new_data):
        if self.head is None:
            self.head = Node(new_data)
            return
        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = Node(new_data)

    #TODO 3: Insert after a specific node
    def insertAfter(self, data, new_data):
        temp = self.head
        while temp.next and temp.data != data:
            temp = temp.next
        if temp.data != data:
            print("node not found")
            return
        new_node = Node(new_data)
        new_node.next = temp.next
        temp.next = new_node

    #TODO 4: Deleting a node at a specific index
    def deleteIndex(self, index):
        # If the linked list is empty, return
        if self.head is None:
            return

        # If the node to be deleted is the head node
        if index == 0:
            self.head = self.head.next
            return

        # Find the previous node of the node to be deleted
        prev_node = None
        current_node = self.head
        count = 0
        while current_node and count != index:
            prev_node = current_node
            current_node = current_node.next
            count += 1

        # If the index is out of range
        if current_node is None:
            print("Index out of range")
            return

        # Unlink the node from the linked list
        prev_node.next = current_node.next

    #TODO 5: Search an element
    def find(self, key):
        # Initialize a pointer to traverse the linked list
        current_node = self.head
        index = 0

        # Traverse the linked list
        while current_node is not None:
            # If the current node's data matches the key, return the index
            if current_node.data == key:
                return index
            # Move to the next node
            current_node = current_node.next
            index += 1

        # If the key is not found, return -1
        return -1

    #TODO 6: Sort the linked list
    #merge sort might have been a bit overkill, oh well.
    def sort(self, head):
        self.head = self.merge_sort(self.head)

    def merge_sort(self, head):
        if not head or not head.next:
            return head

        middle = self.get_middle(head)
        next_to_middle = middle.next
        middle.next = None

        left_half = self.merge_sort(head)
        right_half = self.merge_sort(next_to_middle)

        return self.merge(left_half, right_half)

    def get_middle(self, head):
        slow_pointer = head
        fast_pointer = head

        while fast_pointer.next and fast_pointer.next.next:
            slow_pointer = slow_pointer.next
            fast_pointer = fast_pointer.next.next

        return slow_pointer

    def merge(self, left, right):
        if not left:
            return right
        if not right:
            return left

        if left.data <= right.data:
            result = left
            result.next = self.merge(left.next, right)
        else:
            result = right
            result.next = self.merge(left, right.next)

        return result

    #TODO 7: Print the linked list
    def printList(self):
        current_node = self.head
        while current_node:
            print(current_node.data, end=" -> ")
            current_node = current_node.next
        print("None")
