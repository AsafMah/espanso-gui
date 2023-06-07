import abc
import enum
from dataclasses import dataclass

from nicegui import ui
from msgspec.yaml import decode
from pathlib import Path

from espanso_gui.model import Var, Match, MatchGroup


class ActionEnum(enum.IntEnum):
    ADD_MATCH = enum.auto()
    DELETE_MATCH = enum.auto()
    ADD_VAR = enum.auto()
    DELETE_VAR = enum.auto()


class Action(abc.ABC):
    @abc.abstractmethod
    def do(self):
        pass

    @abc.abstractmethod
    def undo(self):
        pass


class AddMatch(Action):
    def __init__(self, group: list[Match]):
        self.group = group

    def do(self):
        self.group.append(Match())

    def undo(self):
        self.group.pop()


class DeleteMatch(Action):
    def __init__(self, group: list[Match], match_index: int):
        self.group = group
        self.match_index = match_index
        self.match = None

    def do(self):
        self.match = self.group.pop(self.match_index)

    def undo(self):
        self.group.insert(self.match_index, self.match)


class State:
    def __init__(self, groups: list[(str, MatchGroup)]):
        self.groups = groups
        self.action_stack = []
        self.redo_stack = []

    def do(self, action: Action):
        action.do()
        self.action_stack.append(action)

    def undo(self):
        if not self.action_stack:
            return
        action = self.action_stack.pop()
        action.undo()
        self.redo_stack.append(action)

    def redo(self):
        if not self.redo_stack:
            return
        action = self.redo_stack.pop()
        action.do()
        self.action_stack.append(action)


class Ui:
    @staticmethod
    def start():
        files = Path("../test/resources").glob("[!_]*.yml")
        match_groups = [(file.name, decode(file.read_text(), type=MatchGroup)) for file in files]
        Ui(State(match_groups)).run()

    def __init__(self, state: State):
        self.state = state
    @ui.refreshable
    def run(self):
        with ui.row():
            ui.icon('undo', size="xl", color='primary').classes("cursor-pointer").on("click.prevent", lambda: self.state.undo() or self.run.refresh())
            ui.icon('redo', size="xl", color='primary').classes("cursor-pointer").on("click.prevent", lambda: self.state.redo() or self.run.refresh())

        for (name, group) in self.state.groups:
            with ui.row():
                ui.label(name).tailwind.font_weight('extrabold').font_size('3xl')
                with ui.row():
                    self.matches_ui(group)

    @ui.refreshable
    def matches_ui(self, group):
        for i, match in enumerate(group.matches):
            with ui.column():
                with ui.card():
                    self.match_ui(group.matches, match, i)
        with ui.card().classes("cursor-pointer").on("click.prevent", lambda: self.state.do(AddMatch(group.matches)) or self.matches_ui.refresh()):
            ui.icon('add', size="xl", color='primary')

    @ui.refreshable
    def match_ui(self, matches, match, i):
        with ui.row():
            ui.input('Trigger').bind_value(match, "trigger")
            ui.textarea('Replace').bind_value(match, "replace")
            ui.icon('delete', size="xl", color='primary').classes("cursor-pointer").on("click.prevent", lambda: self.state.do(DeleteMatch(matches, i)) or self.matches_ui.refresh())


if __name__ == '__mp_main__':
    Ui.start()

if __name__ == '__main__':
    pass

ui.run()
