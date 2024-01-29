#!python3

from pywebio.input import *
from pywebio.output import *
import json

def number_validate(activity_id: str):
    if not activity_id.isnumeric():
        return "Not a number."
    pass

def not_blank_validate(input_text: str):
    if len(str.split(input_text)) <= 0:
        return "Input is empty."
    pass

def list_not_empty_validate(list: list):
    if len(list) == 0:
        return 'Input list is empty.'
    pass

activity_info = input_group(
    "活动基础信息",
    [
        input("活动id", name="activity_id", validate=number_validate),
        textarea("完全匹配的触发词，每行一个", name = 'equals_keywords_string', validate=not_blank_validate),
        textarea("包含匹配的触发词，每行一个", name='include_keywords_string', validate=not_blank_validate),
        input('挂件个数', name='pendant_count', validate=number_validate),
        input('彩蛋个数', name='egg_count', validate=number_validate)
    ]
)
activity_id, pendant_count, egg_count, equals_keywords_string, include_keywords_string = activity_info['activity_id'], int(activity_info['pendant_count']), int(activity_info['egg_count']), activity_info['equals_keywords_string'], activity_info['include_keywords_string']

# put_text(activity_id)
# put_text(activity_type)

equals_keywords_array = str.split(equals_keywords_string)
include_keywords_array = str.split(include_keywords_string)

effect_range = {
    'effect_danmaku_match_list': equals_keywords_array,
    'effect_danmaku_include_list': include_keywords_array
}

pendant_materials = []
egg_materials = []

for i in range(pendant_count):
    material_info = input_group(
        '输入第' + str(i + 1) + '个挂件物料', [
            input('物料权重', name='probability', type=NUMBER, value=1),
            input('物料宽高比', name='front_material_aspect_ratio', validate=number_validate, value=1),
            input('iOS物料路径', name='front_material_for_ios'),
            input('Android物料路径', name='front_material_for_android'),
            input('iOS兜底URL', name='front_material_url_for_ios'),
            input('Android兜底URL', name='front_material_url_for_android')
        ]
    )
    pendant_materials.append(material_info)

for i in range(egg_count):
    material_info =  input_group(
        '输入第' + str(i + 1) + '个彩蛋物料',
        [
            input('物料权重', name='probability', type=NUMBER, value=1),
            select('iOS物料类型', name='material_type_for_ios', options=[
                {
                    'label': 'Lottie',
                    'value': 1
                }, {
                    'label': 'AlphaPlayer',
                    'value': 2
                }
            ]),
            select('Android物料类型', name='material_type_for_android', options=[
                {
                    'label': 'Lottie',
                    'value': 1
                }, {
                    'label': 'AlphaPlayer',
                    'value': 2
                }
            ]),
            input('物料宽高比', validate=number_validate, name='ratio', value=1),
            input('iOS物料路径', name='material_for_ios'),
            input('Android物料路径', name='material_for_android')
        ]
    )
    egg_materials.append(material_info)

settings_struct = {}
if pendant_count>0:
    pendant_struct = {
        'danmaku_pendant_config': {
            'danmaku_pendant': {
                activity_id: {
                    'danmaku_effect_range': {
                        'effect_danmaku_match_list': equals_keywords_array,
                        'effect_danmaku_include_list': include_keywords_array
                    },
                    'material_list': pendant_materials
                }
            }
        }
    }
    settings_struct.update(pendant_struct)

if egg_count>0:
    egg_struct={
        'danmaku_bonus_scenes': {
            'danmaku_bonus_scenes': {
                activity_id: {
                    'danmaku_effect_range': {
                        'effect_danmaku_match_list': equals_keywords_array,
                        'effect_danmaku_include_list': include_keywords_array
                    },
                    'material_list': egg_materials
                }
            }
        }
    }
    settings_struct.update(egg_struct)

final_struct = {
    'douyin_settings': settings_struct
}
final_json=json.dumps(final_struct, ensure_ascii=False, indent=4)

put_code(content=final_json, language='json')
