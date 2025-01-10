# coding: utf-8

from collections import OrderedDict


def xml_node(name, content, attrs={}):
    return "<%s%s>%s</%s>" % (
        name,
        (" " if attrs else "") + " ".join(['%s="%s"' % (x, attrs[x]) for x in attrs]),
        content,
        name.split(" ")[0],
    )


def dict_to_xml(dic, root="root"):
    def get_attr(some_dic):
        attrs = dict()
        if type(some_dic) in [dict, OrderedDict]:
            for k in some_dic:
                if k and k[0] == "@":
                    attrs[k[1:]] = some_dic[k]
        return attrs

    xml = ""
    for k in dic:
        if not k or k[0] != "@":
            if type(dic[k]) in [dict, OrderedDict]:
                xml += xml_node(
                    k, dict_to_xml(dic[k], root=False), attrs=get_attr(dic[k])
                )
            elif type(dic[k]) is list:
                xml += "".join(
                    [xml_node(k, dict_to_xml(x, root=False)) for x in dic[k]]
                )
            else:
                xml += xml_node(k, dic[k])
    if root:
        return '<?xml version="1.0" encoding="utf-8"?>' + xml_node(
            root, xml.replace("<>", "").replace("</>", ""), attrs=get_attr(dic)
        )
    return xml.replace("<>", "").replace("</>", "")
