-- grant all PRIVILEGES on `MobilePuzzle`.* to 'mobilePuzzle'@'%' identified by 'mobilepuzzle123456';

-- appList
CREATE TABLE `appList` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `appName` varchar(100) NOT NULL COMMENT '应用名称',
  `category` enum('1','2') NOT NULL COMMENT '应用分类 1 iOS，2 android',
  `identifier` varchar(50) NOT NULL COMMENT '应用的标识，如i-anjuke',
  `lastUpdate` int(11) NOT NULL COMMENT '最后更新时间 时间戳',
  `created` int(11) NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='应用列表';

insert into appList values(1,'安居客二手房','1','i-anjuke',1369652004,1369652004),(2,'安居客租房','1','i-haozu2',1369652004,1369652004),(3,'安居客新房','1','i-xinfang',1369652004,1369652004),(4,'安居客金铺','1','i-jinpu',1369652004,1369652004),(5,'安居客经纪人','1','i-broker',1369652004,1369652004),(6,'安居客二手房HD','1','p-anjuke',1369652004,1369652004),(7,'安居客租房HD','1','p-haozu',1369652004,1369652004),(8,'安居客新房HD','1','p-newhome',1369652004,1369652004),(9,'安居客二手房','2','a-anjuke',1369652004,1369652004),(10,'安居客租房','2','a-haozu',1369652004,1369652004),(11,'安居客新房','2','a-xinfang',1369652004,1369652004),(12,'安居客经纪人','2','a-broker',1369652004,1369652004);

-- projectList
create table `projectList`(
`id` int auto_increment comment '主键',
`projectName` varchar(100) not null comment '应用名称',
`appId` int not null comment '应用id',
`lastUpdate` int not null comment '最后更新时间 时间戳',
`created` int not null comment '创建时间',
PRIMARY KEY `id`(`id`)
) ENGINE=innoDB DEFAULT CHARSET=utf8 comment='项目列表' ;

insert into projectList values(1,'安居客二手房3.5',1,1369652004,1369652004);

-- projectEvent
-- create table `projectEvent`(
-- `id` int auto_increment not null comment '主键',
-- `name` varchar(100) not null comment '事件名称',
-- `category` tinyint comment '类型，1:kickoff， 2:api伪接口, 3:api正式移交, 4:切片交付,5:daily build, 6:rc build, 7:真机, 8:Release',
-- `projectId` int not null comment '项目id',
-- `startDate` int not null comment '开始时间',
-- `created` int not null comment '创建时间',
-- `updated` int not null comment '更新时间',
-- primary key `id`(`id`)
-- ) engine=innodb default charset=utf8 comment='项目事件集';

-- codeRepository
create table `codeRepository`(
`id` int auto_increment comment '主键',
`repoName` varchar(100) not null comment '仓库名称',
`repoUrl` varchar(200) not null comment '仓库Url',
`repoHead` varchar(100) not null comment '仓库HEAD SHA1',
`lastUpdate` int not null comment '最后更新时间',
`created` int not null comment '创建时间',
PRIMARY KEY `id`(`id`)
) ENGINE=INNODB default charset=utf8 comment='git仓库信息';

insert into `codeRepository` values (1,'iOS二手房','git@git.corp.anjuke.com:mobile/ios/Anjuke2','18223',1369652004,1369652004),
(2,'iOS好租','git@git.corp.anjuke.com:mobile/ios/Haozu','4f070',1369652004,1369652004),
(3,'iOS新房','git@git.corp.anjuke.com:mobile/ios/aifang','1a461',1369652004,1369652004);


-- appVersionMapper 
create table `appVersionMapper`(
`id` int auto_increment not null comment '主键',
`versionName` VARCHAR(50) not null comment '应用版本,like 3.0,4.0',
`projectId` int not null comment '项目的id',
`lastUpdate` int not null comment '最后更新时间',
`created` int not null comment '创建时间',
primary key`id`(`id`),
index `projectId`(`projectId`)
) engine=innodb default charset=utf8 comment='应用版本对应关系';


-- projectRepoMapper
create table `projectRepoMapper`(
`id` int auto_increment not null comment '主键',
`projectId` int not null comment '项目id',
`repoId` int not null comment '仓库id',
`versionId` int not null comment '版本Id',
`lastUpdate` int not null comment '最后更新时间',
`created` int not null comment '创建时间',
primary key `id`(`id`),
index `projectId`(`projectId`),
index `repoId`(`repoId`)
) ENGINE=innoDb default charset=utf8 comment='项目仓库对应关系表';

-- projectEvent
create table `projectEvent`(
`id` int auto_increment not null comment '主键',
`name` varchar(100) not null comment '事件名称', 
`category` enum('1','2','3', '4', '5', '6', '7', '8', '9', '10') comment '类型，1:backlog, 2:KickOff, 3:PRD交付, 4:api伪接口, 5:api正式移交, 6:切片交付, 7:daily build, 8:rc build, 9:真机, 10:Release ',
`projectId` int not null comment '项目id',
`startDate` int not null comment '开始时间',
`endDate` int not null comment '结束时间',
`created` int not null comment '创建时间',
`updated` int not null comment '更新时间',
primary key `id`(`id`)
) engine=innodb default charset=utf8 comment='项目事件集';

-- uiClipper
create table `uiClipper`(
`id` int auto_increment not null comment '主键',
`name` varchar(100) not null comment '切片名称',
`category` enum('1','2') not  null comment '切片类型',
`picMd5` varchar(100) not null comment '图片MD5码',
`created` int not null comment '创建时间',
`updated` int not null comment '更新时间',
primary key `id`(`id`)
) engine=innodb default charset=utf8 comment='切片列表';










delimiter $$

CREATE TABLE `rp_developer` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `staff_no` varchar(45) NOT NULL,
        `chinese_name` varchar(45) NOT NULL,
        `pmtId` int(11) NOT NULL DEFAULT '0',
        `total` int(11) NOT NULL DEFAULT '0',
        `workload` decimal(10,2) NOT NULL DEFAULT '0.00',
        `unclose` int(11) NOT NULL DEFAULT '0',
        `reopen` int(11) NOT NULL DEFAULT '0',
        `reject` int(11) NOT NULL DEFAULT '0',
        `repair_time` int(11) NOT NULL DEFAULT '0' COMMENT '修复总时间',
        `major_bug` int(11) NOT NULL DEFAULT '0' COMMENT 'p1-p3 bug数',
        `daily_to_rc` int(11) NOT NULL DEFAULT '0' COMMENT 'dailybuild带到rc的bug',
        `rc` int(11) NOT NULL DEFAULT '0' COMMENT 'rc bug',
        `user_from` int(11) NOT NULL COMMENT '1是pmt，2是ibug',
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=627 DEFAULT CHARSET=utf8 COMMENT='开发报表'$$


delimiter $$

CREATE TABLE `rp_projectbug` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `app` int(11) NOT NULL DEFAULT '0' COMMENT 'app bug',
        `api` int(11) NOT NULL DEFAULT '0' COMMENT 'api bug',
        `product` int(11) NOT NULL DEFAULT '0' COMMENT '产品设计bug',
        `p1` int(11) NOT NULL DEFAULT '0',
        `p2` int(11) NOT NULL DEFAULT '0',
        `p3` int(11) NOT NULL DEFAULT '0',
        `p4` int(11) NOT NULL DEFAULT '0',
        `p5` int(11) NOT NULL DEFAULT '0',
        `test` int(11) NOT NULL DEFAULT '0' COMMENT 'daily build bug',
        `dev` int(11) NOT NULL DEFAULT '0' COMMENT 'rc bug',
        `prerelease` int(11) NOT NULL DEFAULT '0' COMMENT '真机测试bug',
        `production` int(11) NOT NULL DEFAULT '0' COMMENT '线上bug',
        `pmtId` int(11) NOT NULL DEFAULT '0',
        `created` int(11) NOT NULL,
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8 COMMENT='项目报表' $$


delimiter $$

CREATE TABLE `rp_projectbug_type` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `type` varchar(45) NOT NULL COMMENT '类型',
        `com_id` int(11) NOT NULL DEFAULT '0' COMMENT '分类id',
        `count` int(11) NOT NULL DEFAULT '0' COMMENT 'bug数量',
        `pmtId` int(11) NOT NULL DEFAULT '0',
        `created` int(11) NOT NULL,
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=3870 DEFAULT CHARSET=utf8 COMMENT='bug 原因和component统计'$$


delimiter $$

CREATE TABLE `rp_qa` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `staff_no` varchar(45) NOT NULL COMMENT '工号',
        `chinese_name` varchar(45) NOT NULL,
        `pmtId` int(11) NOT NULL DEFAULT '0',
        `total` int(11) NOT NULL DEFAULT '0',
        `workload` decimal(10,2) NOT NULL DEFAULT '0.00',
        `p1` int(11) NOT NULL DEFAULT '0',
        `p2` int(11) NOT NULL DEFAULT '0',
        `p3` int(11) NOT NULL DEFAULT '0',
        `p4` int(11) NOT NULL DEFAULT '0',
        `dailybuild` int(11) NOT NULL DEFAULT '0' COMMENT 'daily build bug',
        `user_from` int(11) NOT NULL COMMENT '1是pmt 2是ibug',
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=464 DEFAULT CHARSET=utf8 COMMENT='qa报表'$$


delimiter $$

CREATE TABLE `ticket` (
        `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
        `ticket_id` int(11) NOT NULL,
        `created_at` datetime DEFAULT NULL COMMENT '创建时间',
        `updated_at` datetime DEFAULT NULL COMMENT '最后更新时间',
        `closed_at` datetime DEFAULT NULL COMMENT '关闭时间',
        `priority` varchar(45) DEFAULT NULL COMMENT '优先级',
        `reporter` varchar(45) DEFAULT NULL COMMENT '创建者',
        `owner` varchar(45) DEFAULT NULL COMMENT 'owner',
        `status` varchar(45) DEFAULT NULL COMMENT '状态',
        `summary` varchar(256) NOT NULL COMMENT '摘要',
        `pmtId` int(10) unsigned DEFAULT NULL COMMENT '关联的外部项目id',
        `environment` varchar(45) NOT NULL COMMENT '环境',
        `component` varchar(45) DEFAULT NULL COMMENT '组件',
        `resolution` varchar(45) DEFAULT '' COMMENT '解决的状态',
        `reason` varchar(45) DEFAULT '' COMMENT '解决原因',
        `is_reopen` int(11) DEFAULT '0',
        `is_reject` int(11) DEFAULT '0',
        `is_daily_to_rc` int(11) DEFAULT NULL,
        PRIMARY KEY (`id`,`ticket_id`),
        KEY `reporter` (`reporter`),
        KEY `owner` (`owner`)
    ) ENGINE=InnoDB AUTO_INCREMENT=2310 DEFAULT CHARSET=utf8 COMMENT='ticket信息'$$
