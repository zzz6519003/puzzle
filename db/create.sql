-- grant all PRIVILEGES on `MobilePuzzle`.* to 'mobilePuzzle'@'%' identified by 'mobilepuzzle123456';

-- projectList
create table `projectList`(
`id` int auto_increment comment '主键',
`appName` varchar(100) not null comment '应用名称',
`category` ENUM('1','2') not null comment '应用分类 1 iOS，2 android',
`identifier` varchar(50) not null comment '应用的标识，如i-anjuke',
`lastUpdate` int not null comment '最后更新时间 时间戳',
`created` int not null comment '创建时间',
PRIMARY KEY `id`(`id`)
) ENGINE=innoDB DEFAULT CHARSET=utf8 comment='项目列表' ;

insert into projectList values(1,'安居客二手房','1','i-anjuke',1369652004,1369652004),(2,'安居客租房','1','i-haozu2',1369652004,1369652004),(3,'安居客新房','1','i-xinfang',1369652004,1369652004),(4,'安居客金铺','1','i-jinpu',1369652004,1369652004),(5,'安居客经纪人','1','i-broker',1369652004,1369652004),(6,'安居客二手房HD','1','p-anjuke',1369652004,1369652004),(7,'安居客租房HD','1','p-haozu',1369652004,1369652004),(8,'安居客新房HD','1','p-newhome',1369652004,1369652004),(9,'安居客二手房','2','a-anjuke',1369652004,1369652004),(10,'安居客租房','2','a-haozu',1369652004,1369652004),(11,'安居客新房','2','a-xinfang',1369652004,1369652004),(12,'安居客经纪人','2','a-broker',1369652004,1369652004);

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
`category` enum('1','2','3') comment '类型，1:kickoff， 2:api伪接口, 3:api正式移交, 4:切片交付,5:daily build, 6:rc build, 7:真机, 8:Release ',
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

