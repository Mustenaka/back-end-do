/*
 Navicat Premium Data Transfer

 Source Server         : CatCatGirl
 Source Server Type    : MariaDB
 Source Server Version : 50568
 Source Host           : 159.75.72.254:3306
 Source Schema         : HHM

 Target Server Type    : MariaDB
 Target Server Version : 50568
 File Encoding         : 65001

 Date: 03/05/2021 23:55:13
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for chapters_info
-- ----------------------------
DROP TABLE IF EXISTS `chapters_info`;
CREATE TABLE `chapters_info`  (
  `chaptersId` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '章节ID',
  `subjectId` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '科目ID',
  `chaptersName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '章节名称',
  PRIMARY KEY (`chaptersId`) USING BTREE,
  INDEX `subjectId`(`subjectId`) USING BTREE,
  CONSTRAINT `subjectId` FOREIGN KEY (`subjectId`) REFERENCES `subject_info` (`subjectId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of chapters_info
-- ----------------------------
INSERT INTO `chapters_info` VALUES ('1', '1', '算法绪论（修改）');
INSERT INTO `chapters_info` VALUES ('2', '4', '存储器');
INSERT INTO `chapters_info` VALUES ('3', '2', '指令系统');
INSERT INTO `chapters_info` VALUES ('4', '1', '图');
INSERT INTO `chapters_info` VALUES ('5', '1', '树');

-- ----------------------------
-- Table structure for load_info
-- ----------------------------
DROP TABLE IF EXISTS `load_info`;
CREATE TABLE `load_info`  (
  `userId` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户ID',
  `loadDays` int(255) NOT NULL COMMENT '累计签到天数',
  `lastDay` date NOT NULL COMMENT '上一次签到时间',
  PRIMARY KEY (`userId`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of load_info
-- ----------------------------
INSERT INTO `load_info` VALUES ('10000001', 1, '2021-03-23');
INSERT INTO `load_info` VALUES ('11000002', 5, '2021-03-22');
INSERT INTO `load_info` VALUES ('22000002', 45, '2021-03-23');

-- ----------------------------
-- Table structure for subject_info
-- ----------------------------
DROP TABLE IF EXISTS `subject_info`;
CREATE TABLE `subject_info`  (
  `subjectId` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '科目ID',
  `subjectName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '科目名称',
  `subjectCont` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '科目介绍',
  PRIMARY KEY (`subjectId`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of subject_info
-- ----------------------------
INSERT INTO `subject_info` VALUES ('1', '数据结构与算法', '数据结构是计算机存储、组织数据的方式。数据结构是指相互之间存在一种或多种特定关系的数据元素的集合。通常情况下，精心选择的数据结构可以带来更高的运行或者存储效率。数据结构往往同高效的检索算法和索引技术有关。');
INSERT INTO `subject_info` VALUES ('2', '操作系统', '操作系统（operation system，简称OS）是管理计算机硬件与软件资源的计算机程序。操作系统需要处理如管理与配置内存、决定系统资源供需的优先次序、控制输入设备与输出设备、操作网络与管理文件系统等基本事务。操作系统也提供一个让用户与系统交互的操作界面。');
INSERT INTO `subject_info` VALUES ('3', '计算机网络', '计算机网络是指将地理位置不同的具有独立功能的多台计算机及其外部设备，通过通信线路连接起来，在网络操作系统，网络管理软件及网络通信协议的管理和协调下，实现资源共享和信息传递的计算机系统。');
INSERT INTO `subject_info` VALUES ('4', '计算机组成原理', '计算机组成原理介绍了计算机的基本组成原理和内部工作机制。主要内容分成两个部分：介绍计算机的基础知识；介绍计算机的各子系统（包括运算器、存储器、控制器、外部设备和输入输出子系统等）的基本组成原理、设计方法、相互关系以及各子系统互相连接构成整机系统的技术。');

-- ----------------------------
-- Table structure for title_info
-- ----------------------------
DROP TABLE IF EXISTS `title_info`;
CREATE TABLE `title_info`  (
  `titleId` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '题目ID',
  `titleHead` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '题目标题，如选择题，填空题，特殊题目说明',
  `titleCont` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '题目内容',
  `titleAnswer` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '正确答案-用来验证回答是否正确',
  `titleAnalysis` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '解析-用来查看为什么正确；正确答案和解析不要搞混淆',
  `titleAveracc` int(255) NOT NULL COMMENT '题目平均正确率 - 使用正确回答和错误回答总数进行计算',
  `titleIspaper` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '题目出处',
  `specialNote` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '特殊注释',
  `titleRight` int(255) NOT NULL COMMENT '题目正确回答',
  `titleWrong` int(255) NOT NULL COMMENT '题目错误回答',
  PRIMARY KEY (`titleId`) USING BTREE,
  INDEX `科目号_题目`(`titleCont`) USING BTREE,
  CONSTRAINT `titleId` FOREIGN KEY (`titleId`) REFERENCES `titlenumber_info` (`titleId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of title_info
-- ----------------------------
INSERT INTO `title_info` VALUES ('1', '（单选）一个算法应该是（）', 'A.程序,B.问题求解步骤的描述,C.要满足五个基本属性,D.A和C', 'B', '无', 1, '2018', '无（修改）', 3, 1);
INSERT INTO `title_info` VALUES ('10', '（多选）从逻辑上可以把数据结构分为______两大类', 'A.动态结构,B.线性结构,C.初等结构,D.非线性结构', 'B,D', '数据的逻辑结构是对数据之间关系的描述，从逻辑上可以分为线性结构和非线性结构', 1, '《数据结构C语言版》课后习题', '无', 9, 6);
INSERT INTO `title_info` VALUES ('11', '（单选）在一个无向图中，所有顶点的度数之和等于所有边数的（）倍', 'A.1/2,B.1,C.2,D.4', 'C', '无', 1, '2011', '无', 6, 5);
INSERT INTO `title_info` VALUES ('12', '（单选）在一棵具有5层的满二叉树中结点总数为（）', 'A.31,B.32,C.33,D.16', 'A', 'k层的满二叉树中结点总数为2^K-1', 0, '2012', '无', 1, 3);
INSERT INTO `title_info` VALUES ('13', '(单选）对于一个具有n个顶点的无向连通图，它包含的连通分量的个数是（）', 'A.0,B.1,C.n,D.n+1', 'B', '无', 1, '《数据结构C语言版》课后习题', '无', 2, 1);
INSERT INTO `title_info` VALUES ('2', '（单选）算法分析的两个主要方面是（）', 'A.空间复杂度和时间复杂度,B.正确性和简单性,C.可读性和文档性,D.数据结构复杂性和程序复杂性', 'A', '算法分析的两个主要方面是空间复杂度和时间复杂度', 1, '《数据结构C语言版》课后习题', '无', 5, 0);
INSERT INTO `title_info` VALUES ('3', '（多选）算法的设计要求包括（）', 'A.正确性,B.可读性,C.健壮性,D.确定性', 'A,B,C', '这是一个解析', 0, '《数据结构C语言版》课后习题', '无', 1, 2);
INSERT INTO `title_info` VALUES ('4', '（单选）算法是指的是（）', 'A.计算机程序,B.解决问题的计算方法,C.排序算法,D.解决问题的有限运算序列', 'D', '无', 0, '2016', '无', 1, 5);
INSERT INTO `title_info` VALUES ('7', '（单选）指令系统中采用不同寻址方式的目的是_____', 'A.提高从内存获取数据的速度,B.提高从外存获取数据的速度,C.降低操作码的译码难度,D.扩大寻址空间并提高编程灵活性', 'D', '无', 0, '2016', '无', 2, 15);
INSERT INTO `title_info` VALUES ('8', '（多选）算法的设计要求包括（）', 'A.正确性,B.可读性,C.健壮性,D.确定性', 'A,B,C', '无', 0, '《数据结构C语言版》课后习题', '无', 1, 4);
INSERT INTO `title_info` VALUES ('9', '（单选）下列关于指令系统的描述，正确的是（）', 'A.指令由操作码和控制码两部分组成,B.指令的地址码部分可能是操作数，也可能是操作数的内存单元地址,C.指令的地址码部分是不可缺少的,D.指令的操作码部分描述了完成指令所需要的操作数类型', 'B', '一般的计算机指令包括操作码和操作数：其中操作码指出该指令完成操作的类型；地址码部分可能是操作数，也可能是操作数的内存单元地址', 1, '2015', '无', 6, 5);

-- ----------------------------
-- Table structure for titlenote_info
-- ----------------------------
DROP TABLE IF EXISTS `titlenote_info`;
CREATE TABLE `titlenote_info`  (
  `userId` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户ID',
  `titleId` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '题目ID',
  `isRight` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '回答是否正确',
  `responTime` datetime(0) NOT NULL COMMENT '回答时间',
  `personNote` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '个人笔记',
  PRIMARY KEY (`userId`, `titleId`, `responTime`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of titlenote_info
-- ----------------------------
INSERT INTO `titlenote_info` VALUES ('26152380', '2', '1', '2021-03-29 15:58:16', '有点难');
INSERT INTO `titlenote_info` VALUES ('26152380', '2', '0', '2021-03-29 15:58:20', '有点难');
INSERT INTO `titlenote_info` VALUES ('26152380', '2', '1', '2021-03-29 15:58:23', '有点难');
INSERT INTO `titlenote_info` VALUES ('50672669', '10', '1', '2021-04-20 23:38:12', '');
INSERT INTO `titlenote_info` VALUES ('50672669', '10', '1', '2021-04-20 23:40:29', '');
INSERT INTO `titlenote_info` VALUES ('50672669', '11', '0', '2021-04-20 23:38:28', '');
INSERT INTO `titlenote_info` VALUES ('50672669', '11', '1', '2021-04-20 23:40:37', '');
INSERT INTO `titlenote_info` VALUES ('50672669', '2', '1', '2021-04-20 23:40:47', '');
INSERT INTO `titlenote_info` VALUES ('50672669', '5', '1', '2021-04-20 23:40:52', '');
INSERT INTO `titlenote_info` VALUES ('50672669', '5', '1', '2021-04-21 00:34:03', '');
INSERT INTO `titlenote_info` VALUES ('50672669', '5', '0', '2021-04-21 00:44:17', '');
INSERT INTO `titlenote_info` VALUES ('50672669', '6', '0', '2021-04-21 00:34:11', '');
INSERT INTO `titlenote_info` VALUES ('50672669', '8', '0', '2021-04-20 23:39:38', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '1', '1', '2021-04-22 12:46:00', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '1', '1', '2021-04-22 13:08:43', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '1', '0', '2021-04-23 19:18:57', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '1', '1', '2021-04-24 12:53:41', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '10', '1', '2021-04-22 12:46:39', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '10', '0', '2021-04-22 13:18:16', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '10', '0', '2021-04-23 00:07:25', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '10', '0', '2021-04-23 10:22:59', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '10', '1', '2021-04-23 11:02:14', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '10', '1', '2021-04-23 11:32:01', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '10', '0', '2021-04-23 21:57:30', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '10', '0', '2021-04-23 23:47:01', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '10', '1', '2021-04-23 23:47:18', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '10', '0', '2021-04-24 12:49:31', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '10', '1', '2021-04-24 12:51:09', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '10', '1', '2021-04-24 17:19:28', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '10', '1', '2021-04-27 00:01:38', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '11', '1', '2021-04-22 12:46:48', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '11', '0', '2021-04-22 13:02:56', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '11', '0', '2021-04-22 13:03:05', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '11', '1', '2021-04-23 00:07:31', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '11', '0', '2021-04-23 11:31:55', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '11', '1', '2021-04-23 19:19:34', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '11', '0', '2021-04-23 23:39:22', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '11', '1', '2021-04-23 23:39:38', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '11', '1', '2021-04-24 12:49:37', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '12', '0', '2021-04-23 11:32:05', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '12', '0', '2021-04-23 21:57:34', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '12', '0', '2021-04-24 12:50:18', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '12', '1', '2021-04-24 12:50:45', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '13', '1', '2021-04-23 00:07:35', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '13', '1', '2021-04-24 12:49:42', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '13', '0', '2021-04-24 12:50:01', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '2', '1', '2021-04-22 12:46:10', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '2', '1', '2021-04-22 13:02:49', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '2', '1', '2021-04-24 12:53:48', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '2', '1', '2021-04-24 12:54:01', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '3', '0', '2021-04-22 12:47:18', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '3', '1', '2021-04-23 21:15:02', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '4', '1', '2021-04-22 12:46:17', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '4', '0', '2021-04-22 13:00:10', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '4', '0', '2021-04-22 13:00:15', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '4', '0', '2021-04-24 12:50:30', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '4', '0', '2021-04-24 12:53:57', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '4', '0', '2021-04-24 12:54:16', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '5', '0', '2021-04-22 12:47:31', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '5', '0', '2021-04-22 13:00:18', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '5', '1', '2021-04-22 13:00:32', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '5', '0', '2021-04-22 13:00:45', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '5', '0', '2021-04-23 19:18:25', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '5', '1', '2021-04-23 21:14:46', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '5', '1', '2021-04-24 09:24:10', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '5', '1', '2021-04-24 12:50:14', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '6', '1', '2021-04-22 12:47:40', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '6', '1', '2021-04-22 13:03:01', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '6', '1', '2021-04-22 13:18:03', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '6', '0', '2021-04-23 10:23:03', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '6', '1', '2021-04-23 19:18:28', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '6', '1', '2021-04-23 21:14:50', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '6', '0', '2021-04-24 09:24:16', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '6', '1', '2021-04-24 09:24:53', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '7', '0', '2021-04-22 12:47:51', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '7', '0', '2021-04-22 12:51:08', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '7', '0', '2021-04-22 13:07:57', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '7', '0', '2021-04-22 13:08:07', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '7', '0', '2021-04-23 19:19:28', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '7', '0', '2021-04-23 21:14:05', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '7', '0', '2021-04-23 21:14:22', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '7', '0', '2021-04-23 21:55:54', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '7', '0', '2021-04-23 21:58:09', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '7', '1', '2021-04-23 23:35:48', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '7', '0', '2021-04-23 23:38:52', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '7', '0', '2021-04-23 23:39:32', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '7', '0', '2021-04-23 23:46:44', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '7', '0', '2021-04-23 23:47:13', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '7', '0', '2021-04-24 09:24:31', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '8', '0', '2021-04-22 12:46:59', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '8', '0', '2021-04-23 00:07:39', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '8', '1', '2021-04-24 12:49:56', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '9', '1', '2021-04-22 12:47:59', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '9', '0', '2021-04-22 13:00:12', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '9', '1', '2021-04-22 13:08:03', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '9', '1', '2021-04-22 13:18:07', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '9', '0', '2021-04-23 21:14:12', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '9', '1', '2021-04-23 21:14:26', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '9', '0', '2021-04-23 23:35:53', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '9', '1', '2021-04-23 23:39:10', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '9', '0', '2021-04-23 23:46:54', '');
INSERT INTO `titlenote_info` VALUES ('56554480', '9', '1', '2021-04-24 12:50:59', '');
INSERT INTO `titlenote_info` VALUES ('65665409', '3', '0', '2021-04-19 22:11:38', '');
INSERT INTO `titlenote_info` VALUES ('65665409', '7', '0', '2021-04-19 22:12:24', '');
INSERT INTO `titlenote_info` VALUES ('65665409', '7', '1', '2021-04-19 22:13:06', '');
INSERT INTO `titlenote_info` VALUES ('65665409', '8', '0', '2021-04-19 22:23:57', '');
INSERT INTO `titlenote_info` VALUES ('65665409', '9', '0', '2021-04-19 22:12:45', '');

-- ----------------------------
-- Table structure for titlenumber_info
-- ----------------------------
DROP TABLE IF EXISTS `titlenumber_info`;
CREATE TABLE `titlenumber_info`  (
  `titleId` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '题目ID',
  `chaptersId` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '章节ID',
  PRIMARY KEY (`titleId`) USING BTREE,
  INDEX `chaptersId`(`chaptersId`) USING BTREE,
  CONSTRAINT `chaptersId` FOREIGN KEY (`chaptersId`) REFERENCES `chapters_info` (`chaptersId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of titlenumber_info
-- ----------------------------
INSERT INTO `titlenumber_info` VALUES ('1', '1');
INSERT INTO `titlenumber_info` VALUES ('2', '1');
INSERT INTO `titlenumber_info` VALUES ('4', '1');
INSERT INTO `titlenumber_info` VALUES ('3', '2');
INSERT INTO `titlenumber_info` VALUES ('7', '3');
INSERT INTO `titlenumber_info` VALUES ('9', '3');
INSERT INTO `titlenumber_info` VALUES ('10', '4');
INSERT INTO `titlenumber_info` VALUES ('11', '4');
INSERT INTO `titlenumber_info` VALUES ('13', '4');
INSERT INTO `titlenumber_info` VALUES ('8', '4');
INSERT INTO `titlenumber_info` VALUES ('12', '5');

-- ----------------------------
-- Table structure for user_info
-- ----------------------------
DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info`  (
  `userId` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户唯一ID',
  `userName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户名',
  `userPwd` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '密码',
  `wechatId` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '微信标识符 - 修改后可以不需要',
  `userRightAnswer` int(255) NOT NULL COMMENT '用户回答正确数',
  `userWrongAnswer` int(255) NOT NULL COMMENT '用户回答错误数',
  `isAdministrator` int(255) NOT NULL COMMENT '是否是管理员',
  PRIMARY KEY (`userId`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of user_info
-- ----------------------------
INSERT INTO `user_info` VALUES ('00330151', 'creazytwo', '123123', '00330151', 0, 0, 0);
INSERT INTO `user_info` VALUES ('05620307', 'creazyone', '123123', '05620307', 0, 0, 0);
INSERT INTO `user_info` VALUES ('10000001', 'root', '1231234', '10000001', 112, 108, 1);
INSERT INTO `user_info` VALUES ('10000002', 'secondroot', '123123', '10000002', 101, 45, 1);
INSERT INTO `user_info` VALUES ('10000003', 'admin', '1231234', '10000003', 5, 3, 1);
INSERT INTO `user_info` VALUES ('12189623', 'creazyone', '123123', '12189623', 0, 0, 0);
INSERT INTO `user_info` VALUES ('21248101', '123w', '123w', '21248101', 0, 0, 0);
INSERT INTO `user_info` VALUES ('21346999', 'bbb', 'bbb', '21346999', 0, 0, 0);
INSERT INTO `user_info` VALUES ('26152380', 'hhmisyou', '123123', '26152380', 2, 1, 0);
INSERT INTO `user_info` VALUES ('28283029', 'lyb', '123123', '28283029', 0, 0, 0);
INSERT INTO `user_info` VALUES ('30258132', 'newAccount', '123123', '30258132', 0, 0, 0);
INSERT INTO `user_info` VALUES ('36801636', 'liao2', 'liao12.cd', '36801636', 0, 0, 0);
INSERT INTO `user_info` VALUES ('50672669', 'derwind', '12345678w', '50672669', 6, 4, 0);
INSERT INTO `user_info` VALUES ('50904310', 'liaoyu', 'liao123.om', '50904310', 0, 0, 0);
INSERT INTO `user_info` VALUES ('53161557', 'xiaozzz', 'xiaoxiaoxiao', '53161557', 0, 0, 0);
INSERT INTO `user_info` VALUES ('54952662', 'lioayy', 'liao123.om', '54952662', 0, 0, 0);
INSERT INTO `user_info` VALUES ('56554480', '123www', '123456789hhm', '56554480', 42, 47, 0);
INSERT INTO `user_info` VALUES ('65665409', 'liaomm', 'liao123456', '65665409', 1, 4, 0);
INSERT INTO `user_info` VALUES ('74008946', '123www', '123456789www', '74008946', 0, 0, 0);

SET FOREIGN_KEY_CHECKS = 1;
