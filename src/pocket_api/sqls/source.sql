SET NAMES utf8mb4;

-- sample data

use pocket;

INSERT INTO
    admin_user (
        id,
        email,
        password,
        last_login_ip,
        last_login_time,
        last_logout_time,
        create_at
    )
VALUES (
        1,
        'admin@example.com',
        '!',
        NULL,
        NULL,
        NULL,
        '2026-05-01 10:00:00'
    );

INSERT INTO
    attribute (
        id,
        name,
        create_by,
        modified_by,
        create_at,
        modified_at
    )
VALUES (
        1,
        '电',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        2,
        '草',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        3,
        '火',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        4,
        '一般',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    );

INSERT INTO
    pet_generation (
        id,
        name,
        create_by,
        modified_by,
        create_at,
        modified_at
    )
VALUES (
        1,
        '第一世代',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        2,
        '第二世代',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        3,
        '第三世代',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    );

INSERT INTO
    tag (
        id,
        name,
        color,
        create_by,
        modified_by,
        create_at,
        modified_at
    )
VALUES (
        1,
        '电',
        '#F6C343',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        2,
        '草',
        '#58B368',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        3,
        '火',
        '#F97316',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        4,
        '人气',
        '#EC4899',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    );

INSERT INTO
    pet_egg_group (
        id,
        name,
        create_by,
        modified_by,
        create_at,
        modified_at
    )
VALUES (
        1,
        '陆上',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        2,
        '怪兽',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        3,
        '植物',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    );

INSERT INTO
    pet_feature (
        id,
        introduction,
        detail,
        create_by,
        modified_by,
        create_at,
        modified_at
    )
VALUES (
        1,
        '静电',
        '接触时有概率让对手麻痹。',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        2,
        '茂盛',
        'HP 降低后草属性招式威力会提高。',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        3,
        '猛火',
        'HP 降低后火属性招式威力会提高。',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        4,
        '避雷针',
        '将电属性招式吸引到自己身上。',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    );

INSERT INTO
    pet_rance (
        id,
        p_id,
        name,
        hp,
        attack,
        defense,
        special_attack,
        special_defense,
        speed,
        total,
        is_delete,
        create_by,
        modified_by,
        create_at,
        modified_at
    )
VALUES (
        1,
        NULL,
        '皮卡丘',
        35,
        55,
        40,
        50,
        50,
        90,
        320,
        0,
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        2,
        NULL,
        '妙蛙种子',
        45,
        49,
        49,
        65,
        65,
        45,
        318,
        0,
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        3,
        NULL,
        '小火龙',
        39,
        52,
        43,
        60,
        50,
        65,
        309,
        0,
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    );

INSERT INTO
    pet_skill_category (
        id,
        name,
        create_by,
        modified_by,
        create_at,
        modified_at
    )
VALUES (
        1,
        '物理',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        2,
        '特殊',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        3,
        '变化',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    );

INSERT INTO
    pet_skill (
        id,
        learn_type,
        category_id,
        attribute_id,
        name,
        introduction,
        detail,
        damage,
        aim,
        pp,
        cost_time,
        create_by,
        modified_by,
        create_at,
        modified_at
    )
VALUES (
        1,
        1,
        2,
        1,
        '十万伏特',
        '强力电击攻击对手。',
        '有时会让对手麻痹。',
        90,
        100,
        15,
        0,
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        2,
        1,
        1,
        4,
        '电光一闪',
        '以迅雷不及掩耳之势撞向对手。',
        '必定先制攻击。',
        40,
        100,
        30,
        0,
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        3,
        1,
        2,
        2,
        '飞叶快刀',
        '飞出锋利叶片切斩对手。',
        '容易击中要害。',
        55,
        95,
        25,
        0,
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        4,
        1,
        2,
        3,
        '喷射火焰',
        '放出烈焰攻击对手。',
        '有时会让对手灼伤。',
        90,
        100,
        15,
        0,
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    );

INSERT INTO
    pet_region (
        id,
        p_id,
        name,
        create_by,
        modified_by,
        create_at,
        modified_at
    )
VALUES (
        1,
        NULL,
        '常磐森林',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        2,
        NULL,
        '1号道路',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    );

INSERT INTO
    pet_capture_method (
        id,
        pet_region_id,
        method,
        detail,
        create_by,
        modified_by,
        create_at,
        modified_at
    )
VALUES (
        1,
        1,
        '草丛遇敌',
        '白天',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        2,
        2,
        '草丛遇敌',
        '全天',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    );

INSERT INTO
    pets (
        id,
        name,
        jp_name,
        en_name,
        weight,
        gender_male_ratio,
        base_point_type,
        base_point_value,
        capture_probability,
        egg_hatching_steps,
        create_by,
        modified_by,
        create_at,
        modified_at
    )
VALUES (
        1,
        '皮卡丘',
        'ピカチュウ',
        'Pikachu',
        60,
        50,
        1,
        2,
        190,
        2560,
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        2,
        '妙蛙种子',
        'フシギダネ',
        'Bulbasaur',
        69,
        87,
        2,
        1,
        45,
        5120,
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        3,
        '小火龙',
        'ヒトカゲ',
        'Charmander',
        85,
        87,
        3,
        1,
        45,
        5120,
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    );

INSERT INTO
    pet_image (
        id,
        pet_id,
        image_url,
        sort,
        is_cover,
        create_by,
        modified_by,
        create_at,
        modified_at
    )
VALUES (
        1,
        1,
        '',
        0,
        1,
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        2,
        1,
        '',
        1,
        0,
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        3,
        2,
        '',
        0,
        1,
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        4,
        3,
        '',
        0,
        1,
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    );

INSERT INTO
    pets_pet_generation (pet_id, generation_id)
VALUES (1, 1),
    (2, 1),
    (3, 1);

INSERT INTO
    pets_pet_feature (pet_id, feature_id)
VALUES (1, 1),
    (1, 4),
    (2, 2),
    (3, 3);

INSERT INTO
    pets_pet_rance (pet_id, rance_id)
VALUES (1, 1),
    (2, 2),
    (3, 3);

INSERT INTO
    pets_egg_group (pet_id, egg_group_id)
VALUES (1, 1),
    (2, 2),
    (2, 3),
    (3, 2);

INSERT INTO
    pets_pet_skill (pet_id, skill_id)
VALUES (1, 1),
    (1, 2),
    (2, 3),
    (3, 4);

INSERT INTO
    pets_tag (pet_id, tag_id)
VALUES (1, 1),
    (1, 4),
    (2, 2),
    (3, 3);

INSERT INTO
    pets_pet_region (pet_id, region_id)
VALUES (1, 1),
    (2, 2),
    (3, 2);

INSERT INTO
    item_category (
        id,
        name,
        create_by,
        modified_by,
        create_at,
        modified_at
    )
VALUES (
        1,
        '精灵球',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        2,
        '回复道具',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    );

INSERT INTO
    items (
        id,
        name,
        jp_name,
        en_name,
        introduction,
        detail,
        create_by,
        modified_by,
        create_at,
        modified_at
    )
VALUES (
        1,
        '大师球',
        'マスターボール',
        'Master Ball',
        '必定捕获的精灵球。',
        '对野生宠物使用后一定可以成功捕获。',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        2,
        '伤药',
        'キズぐすり',
        'Potion',
        '回复少量 HP。',
        '常见的基础回复道具。',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        3,
        '高级球',
        'ハイパーボール',
        'Ultra Ball',
        '比超级球更容易捕获宝可梦。',
        '适合中后期使用。',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    );

INSERT INTO
    items_item_category (item_id, category_id)
VALUES (1, 1),
    (2, 2),
    (3, 1);

INSERT INTO
    game_docs (
        id,
        p_id,
        name,
        path,
        content,
        create_by,
        modified_by,
        create_at,
        modified_at
    )
VALUES (
        1,
        NULL,
        '宝可梦朱紫图鉴',
        '/guides/scarlet-violet',
        NULL,
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        2,
        1,
        '帕底亚图鉴总览',
        '/guides/scarlet-violet/paldea-dex',
        '# 帕底亚图鉴总览\n\n- 收录帕底亚地区常见宝可梦\n- 可按区域与编号查看图鉴信息',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        3,
        NULL,
        '对战入门',
        '/guides/battle',
        NULL,
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    ),
    (
        4,
        3,
        '队伍构筑基础',
        '/guides/battle/team-building',
        '# 队伍构筑基础\n\n1. 先确定核心战术\n2. 再补足属性覆盖\n3. 最后检查速度线与耐久',
        1,
        NULL,
        '2026-05-01 10:00:00',
        NULL
    );