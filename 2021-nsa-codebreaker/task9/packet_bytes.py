import time
import base64
import hashlib
import nacl.secret
import nacl.utils

##
## Packet Bytes Constants
##


class PacketBytes:
    def __init__(self):
        self.magic_start = bytes.fromhex("1b4e8197")
        self.magic_end = bytes.fromhex("e02293f2")

        # Params
        self.param_cmd = bytes.fromhex("3d00")  # 00
        self.param_uuid = bytes.fromhex("3d08")  # 08
        self.param_dirname = bytes.fromhex("3d14")  # 20
        self.param_filename = bytes.fromhex("3d1c")  # 28
        self.param_contents = bytes.fromhex("3d20")  # 32
        self.param_more = bytes.fromhex("3d24")  # 36
        self.param_code = bytes.fromhex("3d28")  # 40

        # Non given params
        self.param_add_task = bytes.fromhex("3d18")

        self.params = {
            "cmd": self.param_cmd,
            "uuid": self.param_uuid,
            "dirname": self.param_dirname,
            "command/filename": self.param_filename,
            "result/contents": self.param_contents,
            "more": self.param_more,
            "code": self.param_code,
            # Non given
            "add_task/resultlist": self.param_add_task,
        }

        self.cmd_init = bytes.fromhex("0002")
        self.cmd_tasking_3 = bytes.fromhex("0003")
        self.cmd_tasking_4 = bytes.fromhex("0004")
        self.cmd_tasking_5 = bytes.fromhex("0005")
        self.cmd_upload = bytes.fromhex("0006")
        self.cmd_fin = bytes.fromhex("0007")

        self.commands = {
            "init": self.cmd_init,
            "upload": self.cmd_upload,
            "fin": self.cmd_fin,
            "init_complete": self.cmd_tasking_3,
            "tasking_ready/listdir": self.cmd_tasking_4,
            "next_task_request": self.cmd_tasking_5,
        }

    def compose(self, params):

        ret = b""

        ret += self.magic_start

        # TODO handle null bytes

        for param in params:
            if param[0] == "cmd":
                byte_param = self.param_cmd
                if param[1] in self.commands:
                    argument = self.commands[param[1]]
                else:
                    argument = param[1]
            elif param[0] in self.params and param[0] != "cmd":
                byte_param = self.params[param[0]]
                argument = param[1]

            else:
                byte_param = param[0]
                argument = param[1]

            argument_length = bytes.fromhex(str(hex(len(argument))[2:]).zfill(2))

            if len(argument_length) % 2 != 0:
                argument_length = bytes.fromhex("00") + argument_length

            ret += byte_param
            ret += argument_length
            ret += argument

        ret += self.magic_end

        return ret

    def parse_to_list(self, command_string):
        if command_string.startswith(self.magic_start):
            command_string = command_string[len(self.magic_start) :]
        else:
            return []

        parsed_list = []
        next_param = command_string[:2]

        while True:

            if next_param == bytes.fromhex("e022"):
                return parsed_list

            pc_set = [next_param]
            command_string = command_string[2:]

            # Argument Length
            arg_len = int.from_bytes(command_string[:2], "big")
            pc_set.append(command_string[:2])
            command_string = command_string[2:]

            # Argument
            argument = command_string[:arg_len]
            pc_set.append(argument)

            command_string = command_string[arg_len:]
            parsed_list.append(pc_set)
            next_param = command_string[:2]

    def parse_to_text_list(self, command_string):
        param_lookup = {v: k for k, v in self.params.items()}
        cmd_lookup = {v: k for k, v in self.commands.items()}

        command_string_list = []
        command_list = self.parse_to_list(command_string)

        if len(command_list) > 0:
            next_param = command_list.pop(0)
        else:
            return []

        while True:

            param_list = []
            if next_param[0] in param_lookup:
                param_list.append(param_lookup[next_param[0]])
            else:
                param.list.append(
                    f"unknown_param_{next_param[0].hex()}(".rstrip("\x00")
                )

            # Argument Length
            arg_len = int.from_bytes(next_param[1], "big")
            param_list.append(str(arg_len))

            # Argument
            argument = next_param[2]

            # Function is CMD use lookup
            if (
                next_param[0] in param_lookup
                and param_lookup[next_param[0]] == "cmd"
                and argument in cmd_lookup
            ):
                param_list.append(cmd_lookup[argument])
            else:
                try:
                    param_list.append(
                        f"{argument.decode('utf-8')}".replace("\x00", "<0x00>").replace(
                            "\x0a", "\\n"
                        )
                    )

                except:
                    param_list.appemd(argument.hex())

            command_string_list.append(param_list)

            if len(command_list) > 0:
                next_param = command_list.pop(0)
            else:
                return command_string_list

    def parse_pretty(self, command_string):
        str_list = self.parse_to_text_list(command_string)
        str_out = ""
        for arg in str_list:
            str_out += f"{arg[0]}(l={arg[1]} | {arg[2]}); "
        return str_out


##
## Tests
##

# y = PacketBytes()
# uuid = bytes.fromhex("65f32880f9354863bc9212fd6cadb26e")
# composed = y.compose([["cmd", "init"], ["uuid", uuid]]).hex()

# print(composed)

# assert (
#     composed == "1b4e81973d00000200023d08001065f32880f9354863bc9212fd6cadb26ee02293f2"
# )

# parse1 = y.parse_to_list(
#     bytes.fromhex(
#         "1b4e81973d00000200023d08001065f32880f9354863bc9212fd6cadb26ee02293f2"
#     )
# )
# print(parse1)
# assert parse1 == [
#     [bytes.fromhex("3d00"), bytes.fromhex("0002"), bytes.fromhex("0002")],
#     [
#         bytes.fromhex("3d08"),
#         bytes.fromhex("0010"),
#         bytes.fromhex("65f32880f9354863bc9212fd6cadb26e"),
#     ],
# ]

# parse2 = y.parse_to_text_list(
#     bytes.fromhex("1b4e81973d1800077461736b2d32003d1800077461736b2d3100e02293f2")
# )
# print(parse2)
# assert parse2 == [["add_task", "7", "task-2<0x00>"], ["add_task", "7", "task-1<0x00>"]]


# parse3 = y.parse_pretty(
#     bytes.fromhex(
#         "1b4e81973d14003c2f746d702f656e64706f696e74732f37666130333263622d393764342d343330622d626462652d3835653364343834643863632f7461736b696e6700e02293f2"
#     )
# )
# print(parse3)

# assert (
#     parse3
#     == "dirname(l=60 | /tmp/endpoints/7fa032cb-97d4-430b-bdbe-85e3d484d8cc/tasking<0x00>);"
# )
