# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
def _calc_checksum(data):
    checksum = sum(data)
    return checksum & 0xff

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    oem_write_command = b'\x50\x54'

    print()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
