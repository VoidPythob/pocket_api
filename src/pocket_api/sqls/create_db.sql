create database if not exists pocket
default character set utf8mb4
default collate utf8mb4_unicode_ci;

use pocket;

create table pets (
    `id` int primary key auto_increment comment "宠物id",
    `name` varchar(100) not null unique comment "名称",
    jp_name varchar(100) not null comment "日文名",
    en_name varchar(100) not null comment "英文名",
    `weight` int not null comment "体重",
    gender_male_ratio int comment "雄性性别比例",
    base_point_type int comment "基础点类型",
    base_point_value int comment "基础点数值",
    capture_probability int comment "捕获概率",
    egg_hatching_steps int comment "孵蛋步数",
    create_by int not null comment "创建者",
    modified_by int comment "修改者",
    create_at datetime not null comment "创建于",
    modified_at datetime comment "修改于"
) comment "宠物表";

create table pet_rance (
    `id` int primary key auto_increment comment "种族id",
    p_id int comment "父id",
    `name` varchar(50) comment "种族名",
    hp int comment "血量值",
    attack int comment "攻击值",
    defense int comment "防御值",
    special_attack int comment "特殊攻击值",
    special_defense int comment "特殊防御值",
    speed int comment "速度值",
    total int comment "总计",
    is_delete tinyint not null default 0 comment "是否删除",
    create_by int not null comment "创建者",
    modified_by int comment "修改者",
    create_at datetime not null comment "创建于",
    modified_at datetime comment "修改于"
) comment "宠物种族表";

create table pet_feature (
    `id` int primary key auto_increment comment "特性id",
    introduction varchar(100) comment "特性简介",
    detail varchar(500) comment "特性详情",
    create_by int not null comment "创建者",
    modified_by int comment "修改者",
    create_at datetime not null comment "创建于",
    modified_at datetime comment "修改于"
) comment "宠物特性表";

create table pet_egg_group (
    `id` int primary key auto_increment comment "蛋组id",
    `name` varchar(50) not null comment "蛋组名字",
    create_by int not null comment "创建者",
    modified_by int comment "修改者",
    create_at datetime not null comment "创建于",
    modified_at datetime comment "修改于"
) comment "宠物蛋组";

create table pet_generation (
    `id` int primary key auto_increment comment "世代id",
    `name` varchar(50) not null comment "世代名称",
    create_by int not null comment "创建者",
    modified_by int comment "修改者",
    create_at datetime not null comment "创建于",
    modified_at datetime comment "修改于"
) comment "宠物世代表";

create table pet_capture_method (
    `id` int primary key auto_increment comment "宠物捕获方式id",
    pet_region_id int comment "捕获地点id",
    `method` varchar(100) comment "捕获方法",
    detail varchar(20) comment "捕获详细说明",
    create_by int not null comment "创建者",
    modified_by int comment "修改者",
    create_at datetime not null comment "创建于",
    modified_at datetime comment "修改于"
) comment "宠物捕获方式";

create table pet_skill (
    `id` int primary key auto_increment comment "宠物技能id",
    learn_type tinyint comment "学习类型",
    category_id int comment "技能分类id",
    attribute_id int comment "属性id",
    `name` varchar(100) comment "技能名称",
    introduction varchar(100) comment "技能简介",
    detail varchar(100) comment "技能详细",
    damage int comment "伤害值",
    aim int comment "命中值",
    pp int comment "力量值",
    cost_time int comment "耗时间",
    create_by int not null comment "创建者",
    modified_by int comment "修改者",
    create_at datetime not null comment "创建于",
    modified_at datetime comment "修改于"
) comment "宠物技能";

create table pet_skill_affected (
    pet_skill_id int primary key comment "技能id",
    is_touch tinyint comment "接触类",
    defense tinyint comment "受守住影响",
    magic_reflect tinyint comment "受魔法反射影响",
    learn_speech tinyint comment "受学舌影响",
    proof_of_king tinyint comment "受王者之证影响"
) comment "宠物技能被影响表";

create table pet_skill_category (
    `id` int primary key auto_increment,
    `name` varchar(50) comment "技能分类名",
    create_by int not null comment "创建者",
    modified_by int comment "修改者",
    create_at datetime not null comment "创建于",
    modified_at datetime comment "修改于"
) comment "宠物技能分类表";

create table pet_guide (
    pet_id int primary key comment "宠物id",
    detail varchar(50) comment "图鉴详细",
    create_by int not null comment "创建者",
    modified_by int comment "修改者",
    create_at datetime not null comment "创建于",
    modified_at datetime comment "修改于"
) comment "宠物图鉴";

create table pet_image (
    `id` int primary key auto_increment comment "宠物图片id",
    pet_id int not null comment "宠物id",
    image_url varchar(255) not null comment "图片地址",
    sort int not null default 0 comment "排序值",
    is_cover tinyint not null default 0 comment "是否封面",
    create_by int not null comment "创建者",
    modified_by int comment "修改者",
    create_at datetime not null comment "创建于",
    modified_at datetime comment "修改于",
    unique key uk_pet_image (pet_id, image_url),
    index idx_pet_id (pet_id),
    index idx_cover (pet_id, is_cover)
) comment "宠物图片表";

create table pet_region (
    `id` int primary key auto_increment comment "宠物地区",
    p_id int comment "父id",
    `name` varchar(50) comment "地区名",
    create_by int not null comment "创建者",
    modified_by int comment "修改者",
    create_at datetime not null comment "创建于",
    modified_at datetime comment "修改于"
) comment "宠物地区";

create table `attribute` (
    `id` int primary key auto_increment comment "属性id",
    `name` varchar(10) comment "属性名",
    create_by int not null comment "创建者",
    modified_by int comment "修改者",
    create_at datetime not null comment "创建于",
    modified_at datetime comment "修改于"
) comment "属性";

create table items (
    `id` int primary key auto_increment comment "物品id",
    `name` varchar(100) not null comment "名称",
    jp_name varchar(100) comment "日文名",
    en_name varchar(100) comment "英语名",
    introduction varchar(100) comment "物品介绍",
    detail varchar(500) comment "物品详情",
    create_by int not null comment "创建者",
    modified_by int comment "修改者",
    create_at datetime not null comment "创建于",
    modified_at datetime comment "修改于"
) comment "物品";

create table item_category (
    `id` int primary key auto_increment comment "物品分类id",
    `name` varchar(20) comment "分类名",
    create_by int not null comment "创建者",
    modified_by int comment "修改者",
    create_at datetime not null comment "创建于",
    modified_at datetime comment "修改于"
) comment "物品分类";

create table tag (
    `id` int primary key auto_increment comment "标签id",
    `name` varchar(50) not null unique comment "标签名",
    `color` varchar(20) comment "标签颜色",
    create_by int not null comment "创建者",
    modified_by int comment "修改者",
    create_at datetime not null comment "创建于",
    modified_at datetime comment "修改于"
) comment "标签表";

create table game_docs (
    `id` int primary key auto_increment comment "文档id",
    p_id int comment "文档父id",
    `name` varchar(100) comment "文档名称",
    `path` varchar(100) comment "文档路径",
    `content` text comment "Markdown文档内容",
    create_by int not null comment "创建者",
    modified_by int comment "修改者",
    create_at datetime not null comment "创建于",
    modified_at datetime comment "修改于"
) comment "游戏文档";

create table admin_user (
    `id` int primary key auto_increment comment "管理员用户id",
    email varchar(50) not null unique comment "邮箱",
    `password` varchar(128) not null comment "密码",
    last_login_ip varchar(50) comment "上次登录ip",
    last_login_time datetime comment "上次登录时间",
    last_logout_time datetime comment "上次登出时间",
    create_at datetime comment "创建时间",
    index idx_email (email) comment "邮箱索引"
) comment "管理员用户";

create table pets_attribute (
    pet_id int not null comment '宠物ID',
    attribute_id int not null comment '属性ID',
    primary key (pet_id, attribute_id),
    index idx_attribute_id (attribute_id)
) comment '宠物属性关联表';

create table pets_pet_rance (
    pet_id int not null comment '宠物ID',
    rance_id int not null comment '稀有度ID',
    primary key (pet_id, rance_id),
    index idx_rance_id (rance_id)
) comment '宠物稀有度关联表';

create table pets_pet_feature (
    pet_id int not null comment '宠物ID',
    feature_id int not null comment '特性ID',
    primary key (pet_id, feature_id),
    index idx_feature_id (feature_id)
) comment '宠物特性关联表';

create table pets_egg_group (
    pet_id int not null comment '宠物ID',
    egg_group_id int not null comment '蛋组ID',
    primary key (pet_id, egg_group_id),
    index idx_egg_group_id (egg_group_id)
) comment '宠物蛋组关联表';

create table pets_pet_generation (
    pet_id int not null comment '宠物ID',
    generation_id int not null comment '世代ID',
    primary key (pet_id, generation_id),
    index idx_generation_id (generation_id)
) comment '宠物世代关联表';

create table pets_pet_skill (
    pet_id int not null comment '宠物ID',
    skill_id int not null comment '技能ID',
    primary key (pet_id, skill_id),
    index idx_skill_id (skill_id)
) comment '宠物技能关联表';

create table pets_tag (
    pet_id int not null comment '宠物ID',
    tag_id int not null comment '标签ID',
    primary key (pet_id, tag_id),
    index idx_tag_id (tag_id)
) comment '宠物标签关联表';

create table pets_pet_guide (
    pet_id int not null comment '宠物ID',
    guide_id int not null comment '攻略ID',
    primary key (pet_id, guide_id),
    index idx_guide_id (guide_id)
) comment '宠物攻略关联表';

create table pets_pet_region (
    pet_id int not null comment '宠物ID',
    region_id int not null comment '地区ID',
    primary key (pet_id, region_id),
    index idx_region_id (region_id)
) comment '宠物地区分布关联表';

create table pet_skill_attribute (
    pet_skill_id int not null comment '宠物技能ID',
    attribute_id int not null comment '属性ID',
    primary key (pet_skill_id, attribute_id),
    index idx_attribute_id (attribute_id)
) comment '宠物技能属性关联表';

create table items_item_category (
    item_id int not null comment '物品ID',
    category_id int not null comment '分类ID',
    primary key (item_id, category_id),
    index idx_category_id (category_id)
) comment '物品分类关联表';
