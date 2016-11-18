##
# Copyright (c) 2016 MagicStack Inc.
# All rights reserved.
#
# See LICENSE for details.
##


import re

from edgedb.lang.common import ast, parsing


class Base(ast.AST):
    ns = 'graphql'
    __fields = [('context', parsing.ParserContext, None,
                 True, None, True  # this last True is "hidden" attribute
                 )]

    def _extra_repr(self):
        return ''

    def __repr__(self):
        ar = self._extra_repr()
        return '<{}.{} at {:#x}{}>'.format(self.__class__.ns,
                                           self.__class__.__name__,
                                           id(self),
                                           ar)


class LiteralNode(Base):
    __fields = ['value']

    def topython(self):
        return self.value


class StringLiteral(LiteralNode):
    def tosource(self):
        value = self.value
        # generic substitutions for '\b' and '\f'
        #
        value = value.replace('\b', '\\b').replace('\f', '\\f')
        value = repr(value)
        # escape \b \f \u1234 and \/ correctly
        #
        value = re.sub(r'\\\\([fb])', r'\\\1', value)
        value = re.sub(r'\\\\(u[0-9a-fA-F]{4})', r'\\\1', value)
        value = value.replace('/', r'\/')

        if value[0] == "'":
            # need to change quotation style
            #
            value = value[1:-1].replace(R'\'', "'").replace('"', R'\"')
            value = '"' + value + '"'

        return value


class IntegerLiteral(LiteralNode):
    pass


class FloatLiteral(LiteralNode):
    pass


class BooleanLiteral(LiteralNode):
    pass


class EnumLiteral(LiteralNode):
    pass


class ListLiteral(LiteralNode):
    def topython(self):
        return [val.topython() for val in self.value]


class ObjectLiteral(LiteralNode):
    def topython(self):
        return {field.name: field.value.topython() for field in self.value}


class Variable(Base):
    __fields = ['value']


class Document(Base):
    __fields = [('definitions', list, list)]


class Definition(Base):
    __fields = [
        ('name', str, None),
        'selection_set',
    ]


class OperationDefinition(Definition):
    __fields = [
        ('type', str, None),
        ('variables', list, list),
        ('directives', list, list),
    ]


class FragmentDefinition(Definition):
    __fields = [
        'on',
        ('directives', list, list),
    ]


class VariableDefinition(Base):
    __fields = ['name', 'type', 'value']


class VariableType(Base):
    __fields = [
        'name',
        ('nullable', bool, True),
        ('list', bool, False),
    ]


class SelectionSet(Base):
    __fields = [('selections', list, list)]


class Selection(Base):
    pass


class Field(Selection):
    __fields = [
        ('alias', str, None),
        'name',
        ('arguments', list, list),
        ('directives', list, list),
        'selection_set',
    ]


class FragmentSpread(Selection):
    __fields = [
        'name',
        ('directives', list, list),
    ]


class InlineFragment(Selection):
    __fields = [
        'on',
        ('directives', list, list),
        'selection_set',
    ]


class Directive(Base):
    __fields = [
        'name',
        ('arguments', list, list),
    ]


class Argument(Base):
    __fields = ['name', 'value']


class ObjectField(Base):
    __fields = ['name', 'value']
