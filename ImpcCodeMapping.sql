USE `komp`;
DROP procedure IF EXISTS `updateDccParam`;

USE `komp`;
DROP procedure IF EXISTS `komp`.`updateDccParam`;
;

DELIMITER $$
USE `komp`$$
CREATE DEFINER=`dba`@`%` PROCEDURE `updateDccParam`(IN ClimbKey INT, IN ImpCodeStr VARCHAR(32))
BEGIN
	UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=ClimbKey WHERE ImpcCode = ImpCodeStr ;
END$$

DELIMITER ;
;

DROP TABLE IF EXISTS `komp`.`cv_dcctype` ;
CREATE TABLE `komp`.`cv_dcctype` (
  `_DccType_key` int(11) NOT NULL AUTO_INCREMENT,
  `TypeName` varchar(16) NOT NULL,
  PRIMARY KEY (`_DccType_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `komp`.`cv_dcctype` (`_DccType_key`,`TypeName`)
VALUES
(	1,	'Simple' ),
(	2,	'Ontology'	),
(	3,	'Media'	),
(	4,	'Series'	),
(	5,	'SeriesMedia'	),
(	6,	'MediaSample'	),
(	7,	'Metadata'	);

DROP TABLE IF EXISTS `komp`.`dccparameterdetails` ;
CREATE TABLE `komp`.`dccparameterdetails` (
  `_DccParameterDetails_key` int(11) NOT NULL AUTO_INCREMENT,
  `_Workgroup_key` int(11) NOT NULL DEFAULT '17',
  `_DccType_key` int(11) NOT NULL,
  `ImpcCode` varchar(32) DEFAULT NULL,
  `IsActive` smallint(6) NOT NULL DEFAULT '1',
  `IsRequired` smallint(6) NOT NULL DEFAULT '0',
  `IsDate` smallint(6) NOT NULL DEFAULT '0',
  `IsTime` smallint(6) NOT NULL DEFAULT '0',
  `IsDateTime` smallint(6) NOT NULL DEFAULT '0',
  `IsIncremented` smallint(6) NOT NULL DEFAULT '0',
  `IncrementStartValue` int(11) DEFAULT '1',
  `IncrementValue` int(11) DEFAULT '1',
  `IsSupported` int(11) DEFAULT '1',
  `IsAssociated` smallint(6) NOT NULL DEFAULT '0',
  `CreatedBy` varchar(128) NOT NULL,
  `DateCreated` datetime NOT NULL,
  `ModifiedBy` varchar(128) NOT NULL,
  `DateModified` datetime NOT NULL,
  `Version` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`_DccParameterDetails_key`),
  KEY `_DccType_key` (`_DccType_key`),
  KEY `idx_dccparameterdetails_ImpcCode` (`ImpcCode`),
  CONSTRAINT `DccParameterDetails_ibfk_1` FOREIGN KEY (`_DccType_key`) REFERENCES `cv_dcctype` (`_DccType_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `komp`.`taskimpccodes` ;
CREATE TABLE `komp`.`taskimpccodes` (
  `_TaskImpcCodes_key` int(11) NOT NULL AUTO_INCREMENT,
  `TaskName`  varchar(64) DEFAULT NULL,
  `ImpcCode` varchar(32) DEFAULT NULL,
  `IsActive` smallint(6) NOT NULL DEFAULT '1',
  `CreatedBy` varchar(128) NOT NULL,
  `DateCreated` datetime NOT NULL,
  `ModifiedBy` varchar(128) NOT NULL,
  `DateModified` datetime NOT NULL,
  `Version` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`_TaskImpcCodes_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `komp`.`taskimpccodes`
(TaskName, ImpcCode,IsActive,CreatedBy,DateCreated,ModifiedBy, DateModified, Version)
VALUES
('Body Weight','IMPC_BWT_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('First Body Weight','IMPC_BWT_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('SHIRPA','IMPC_CSD_003',1,'michaelm',NOW(),'michaelm',NOW(),1),
('Dysmorphology','IMPC_CSD_003',1,'michaelm',NOW(),'michaelm',NOW(),1),
('Open Field','JAX_OFD_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('Light/Dark','JAX_LDT_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('Holeboard','JAX_HBD_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('Eye Morphology','IMPC_EYE_003',1,'michaelm',NOW(),'michaelm',NOW(),1),
('GTT','IMPC_IGP_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('ABR','JAX_ABR_002',1,'michaelm',NOW(),'michaelm',NOW(),1),
('EKGv3','IMPC_ECG_003',1,'michaelm',NOW(),'michaelm',NOW(),1),
('ERGv2','JAX_ERG_002',1,'michaelm',NOW(),'michaelm',NOW(),1),
('Heart Weight','IMPC_HWT_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('Clinical Blood Chemistry','IMPC_CBC_003',1,'michaelm',NOW(),'michaelm',NOW(),1),
('Hematology','IMPC_HEM_002',1,'michaelm',NOW(),'michaelm',NOW(),1),
('Grip Strength','IMPC_GRS_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('Startle/PPI','IMPC_ACS_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('Body Composition','IMPC_DXA_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('Primary Viability Screen','IMPC_VIA_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('E9.5 Embryo Gross Morphology','IMPC_GEL_003',1,'michaelm',NOW(),'michaelm',NOW(),1),
('E12.5 Embryo Gross Morphology','IMPC_GEM_003',1,'michaelm',NOW(),'michaelm',NOW(),1),
('E15.5 Embryo Gross Morphology','IMPC_GEP_003',1,'michaelm',NOW(),'michaelm',NOW(),1),
('E18.5 Embryo Gross Morphology','IMPC_GEO_003',1,'michaelm',NOW(),'michaelm',NOW(),1),
('E9.5 Gross Morphology Placenta E9.5','IMPC_GPL_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('E12.5 Gross Morphology Placenta','IMPC_GPM_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('E15.5 Gross Morphology Placenta','IMPC_GPP_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('E18.5 Gross Morphology Placenta','IMPC_GPO_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('Viability E9.5 Secondary Screening','IMPC_EVL_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('Viability E12.5 Secondary Screening','IMPC_EVM_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('Viability E15.5 Secondary Screening','IMPC_EVP_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('Viability E18.5 Secondary Screening','IMPC_EVO_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('Fertility','IMPC_FER_001',1,'michaelm',NOW(),'michaelm',NOW(),1),
('MicroCT 18.5','IMPC_EMA_002',1,'michaelm',NOW(),'michaelm',NOW(),1),
('Welfare Observations','IMPC_WEL_001',1,'michaelm',NOW(),'michaelm',NOW(),1);


INSERT INTO `komp`.`dccparameterdetails` SELECT * FROM `rslims`.`dccparameterdetails` WHERE ImpcCode NOT LIKE '%JAXLA%'; 
ALTER TABLE `komp`.`dccparameterdetails`  ADD COLUMN _ClimbType_key INT AFTER _Workgroup_key;
ALTER TABLE `komp`.`dccparameterdetails`  ADD COLUMN IsInput TINYINT AFTER _ClimbType_key;

UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=251 WHERE ImpcCode = 'IMPC_ABR_042_001';  -- ABR - Auditory Brain Stem ResponseAnaesthetic agent 1
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=252 WHERE ImpcCode = 'IMPC_ABR_044_001';  -- ABR - Auditory Brain Stem ResponseAnaesthetic dose 1
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=254 WHERE ImpcCode = 'IMPC_ABR_045_001';  -- ABR - Auditory Brain Stem ResponseAnaesthetic dose 2
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=255 WHERE ImpcCode = 'IMPC_ABR_046_001';  -- ABR - Auditory Brain Stem ResponseAnesthetic administration route
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=253 WHERE ImpcCode = 'IMPC_ABR_043_001';  -- ABR - Auditory Brain Stem ResponseAnesthetic agent 2
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=241 WHERE ImpcCode = 'IMPC_ABR_049_001';  -- ABR - Auditory Brain Stem ResponseEquipment ID 
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=240 WHERE ImpcCode = 'IMPC_ABR_050_001';  -- ABR - Auditory Brain Stem ResponseEquipment Mfg
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=242 WHERE ImpcCode = 'IMPC_ABR_051_001';  -- ABR - Auditory Brain Stem ResponseEquipment model
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=236 WHERE ImpcCode = 'IMPC_ABR_053_001';  -- ABR - Auditory Brain Stem ResponseExperimenter
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=239 WHERE ImpcCode = 'IMPC_ABR_054_001';  -- ABR - Auditory Brain Stem ResponseLast calibration date
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=250 WHERE ImpcCode = 'IMPC_ABR_040_001';  -- ABR - Auditory Brain Stem ResponseNumber Averages
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=246 WHERE ImpcCode = 'IMPC_ABR_028_001';  -- ABR - Auditory Brain Stem ResponseRange of test stimuli used
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=244 WHERE ImpcCode = 'IMPC_ABR_041_001';  -- ABR - Auditory Brain Stem ResponseRecording environment
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=249 WHERE ImpcCode = 'IMPC_ABR_039_001';  -- ABR - Auditory Brain Stem ResponseRepetition Rates
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=243 WHERE ImpcCode = 'IMPC_ABR_052_001';  -- ABR - Auditory Brain Stem ResponseSoftware
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=245 WHERE ImpcCode = 'IMPC_ABR_036_001';  -- ABR - Auditory Brain Stem ResponseStimulus level step size
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=237 WHERE ImpcCode = 'IMPC_ABR_048_001';  -- ABR - Auditory Brain Stem ResponseTime of day
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=247 WHERE ImpcCode = 'IMPC_ABR_037_001';  -- ABR - Auditory Brain Stem ResponseTone Pip Duration
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=248 WHERE ImpcCode = 'IMPC_ABR_038_001';  -- ABR - Auditory Brain Stem ResponseTone-Pip Rise/Fall
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=163 WHERE ImpcCode = 'IMPC_DXA_011_001';  -- Body CompositionEquipment Name
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=164 WHERE ImpcCode = 'IMPC_DXA_012_001';  -- Body CompositionEquipment Manufacturer
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=165 WHERE ImpcCode = 'IMPC_DXA_013_001';  -- Body CompositionEquipment Model
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=166 WHERE ImpcCode = 'IMPC_DXA_014_001';  -- Body CompositionMouse Status
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=167 WHERE ImpcCode = 'IMPC_DXA_015_001';  -- Body CompositionAnesthesia
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=168 WHERE ImpcCode = 'IMPC_DXA_016_001';  -- Body CompositionExperimenter ID
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=44 WHERE ImpcCode = 'IMPC_BWT_005_001';  -- Body WeightExperimenter
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=45 WHERE ImpcCode = 'IMPC_BWT_003_001';  -- Body WeightEquipment Name
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=46 WHERE ImpcCode = 'IMPC_BWT_004_001';  -- Body WeightEquipment Manufacturer
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=47 WHERE ImpcCode = 'IMPC_BWT_007_001';  -- Body WeightEquipment model
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=224 WHERE ImpcCode = 'IMPC_CBC_051_001';  -- Clinical Blood ChemistryAnalyst ID
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=207 WHERE ImpcCode = 'IMPC_CBC_036_001';  -- Clinical Blood ChemistryAnathesia Used for Blood Collection
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=209 WHERE ImpcCode = 'IMPC_CBC_038_001';  -- Clinical Blood ChemistryAnticoagulant
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=221 WHERE ImpcCode = 'IMPC_CBC_039_001';  -- Clinical Blood ChemistryBlood collection tubes
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=217 WHERE ImpcCode = 'IMPC_CBC_046_001';  -- Clinical Blood ChemistryDate and time of Blood Collection
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=222 WHERE ImpcCode = 'IMPC_CBC_040_001';  -- Clinical Blood ChemistryDate and time of sacrifice
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=205 WHERE ImpcCode = 'IMPC_CBC_034_001';  -- Clinical Blood ChemistryEquipment Manufacturer
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=206 WHERE ImpcCode = 'IMPC_CBC_035_001';  -- Clinical Blood ChemistryEquipment Model
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=204 WHERE ImpcCode = 'IMPC_CBC_033_001';  -- Clinical Blood ChemistryEquipment Name
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=220 WHERE ImpcCode = 'IMPC_CBC_049_001';  -- Clinical Blood ChemistryExperimenter ID
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=210 WHERE ImpcCode = 'IMPC_CBC_057_001';  -- Clinical Blood ChemistryFasting
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=219 WHERE ImpcCode = 'IMPC_CBC_048_001';  -- Clinical Blood ChemistryHemolysis Status (enum)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=216 WHERE ImpcCode = 'IMPC_CBC_045_001';  -- Clinical Blood ChemistryID of Blood Collection SOP
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=208 WHERE ImpcCode = 'IMPC_CBC_037_001';  -- Clinical Blood ChemistryMethod of Blood Collection
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=215 WHERE ImpcCode = 'IMPC_CBC_044_001';  -- Clinical Blood ChemistryPlasma Dilution
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=227 WHERE ImpcCode = 'IMPC_CBC_059_001';  -- Clinical Blood ChemistryReagent Manufacturer
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=214 WHERE ImpcCode = 'IMPC_CBC_043_001';  -- Clinical Blood ChemistrySample Status
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=226 WHERE ImpcCode = 'IMPC_CBC_056_001';  -- Clinical Blood ChemistrySample Type
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=213 WHERE ImpcCode = 'IMPC_CBC_042_001';  -- Clinical Blood ChemistrySamples Kept on Ice Between Collection adn Analysis
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=223 WHERE ImpcCode = 'IMPC_CBC_041_001';  -- Clinical Blood ChemistryStorage temperature from blood collection till measurement
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=143 WHERE ImpcCode = 'IMPC_ECG_016_001';  -- EKG v3Equipment ID
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=144 WHERE ImpcCode = 'IMPC_ECG_017_001';  -- EKG v3Equipment Manufacturer
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=145 WHERE ImpcCode = 'IMPC_ECG_018_001';  -- EKG v3Equipment Model
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=146 WHERE ImpcCode = 'IMPC_ECG_019_001';  -- EKG v3Anesthetic
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=147 WHERE ImpcCode = 'IMPC_ECG_020_001';  -- EKG v3Analyst ID
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=151 WHERE ImpcCode = 'IMPC_ECG_030_001';  -- EKG v3Data acquisition sampling rate
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=264 WHERE ImpcCode = 'JAX_ERG_035_001';  -- ERG v2.0C-Wave (cd.s/m²)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=256 WHERE ImpcCode = 'JAX_ERG_029_001';  -- ERG v2.0Experimenter
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=265 WHERE ImpcCode = 'JAX_ERG_036_001';  -- ERG v2.0Photopic ERG (cd.s/m²)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=260 WHERE ImpcCode = 'JAX_ERG_032_001';  -- ERG v2.0Software Version
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=261 WHERE ImpcCode = 'JAX_ERG_033_001';  -- ERG v2.0SOP Version
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=262 WHERE ImpcCode = 'JAX_ERG_034_001';  -- ERG v2.0Stimulator
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=258 WHERE ImpcCode = 'JAX_ERG_030_001';  -- ERG v2.0Stimulus Protocol
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=259 WHERE ImpcCode = 'JAX_ERG_031_001';  -- ERG v2.0Topical Agents
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=172 WHERE ImpcCode = 'IMPC_EYE_030_001';  -- Eye MorphologySlit Lamp Equipment ID
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=173 WHERE ImpcCode = 'IMPC_EYE_031_001';  -- Eye MorphologySlit Lamp Equipment Mfg
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=174 WHERE ImpcCode = 'IMPC_EYE_032_001';  -- Eye MorphologySlit Lamp Model
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=175 WHERE ImpcCode = 'IMPC_EYE_033_001';  -- Eye MorphologyOphthalmoscope Equip ID
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=176 WHERE ImpcCode = 'IMPC_EYE_034_001';  -- Eye MorphologyOphthalmoscope Equip Mfg
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=177 WHERE ImpcCode = 'IMPC_EYE_035_001';  -- Eye MorphologyOphthalmoscope Equip Model
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=178 WHERE ImpcCode = 'IMPC_EYE_043_001';  -- Eye MorphologyDilation Method
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=179 WHERE ImpcCode = 'IMPC_EYE_044_001';  -- Eye MorphologyTopical Anesthetic
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=180 WHERE ImpcCode = 'IMPC_EYE_045_001';  -- Eye MorphologyGeneral Anesthetic
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=181 WHERE ImpcCode = 'IMPC_EYE_046_001';  -- Eye MorphologySlit Lamp Last Calibrated
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=182 WHERE ImpcCode = 'IMPC_EYE_047_001';  -- Eye MorphologyOphthalmoscope Last Calibrated
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=171 WHERE ImpcCode = 'IMPC_EYE_036_001';  -- Eye MorphologyExperimenter ID
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=39 WHERE ImpcCode = 'IMPC_BWT_005_001';  -- First body weightExperimenter
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=40 WHERE ImpcCode = 'IMPC_BWT_003_001';  -- First body weightEquipment Name
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=41 WHERE ImpcCode = 'IMPC_BWT_004_001';  -- First body weightEquipment Manufacturer
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=42 WHERE ImpcCode = 'IMPC_BWT_007_001';  -- First body weightEquipment model
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=78 WHERE ImpcCode = 'IMPC_GRS_012_001';  -- Grip StrengthExperimenter
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=84 WHERE ImpcCode = 'IMPC_GRS_005_001';  -- Grip StrengthEquipment ID
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=85 WHERE ImpcCode = 'IMPC_GRS_006_001';  -- Grip StrengthEquipment Mfg
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=86 WHERE ImpcCode = 'IMPC_GRS_013_001';  -- Grip StrengthEquipment Model
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=88 WHERE ImpcCode = 'IMPC_GRS_007_001';  -- Grip StrengthGrid Mfg
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=89 WHERE ImpcCode = 'IMPC_GRS_014_001';  -- Grip StrengthDate last calibrated
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=157 WHERE ImpcCode = 'IMPC_IPG_008_001';  -- Glucose Tolerance TestExperimenter ID
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=161 WHERE ImpcCode = 'IMPC_IPG_013_001';  -- Glucose Tolerance TestUpper limit of the meter
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=152 WHERE ImpcCode = 'IMPC_IPG_003_001';  -- Glucose Tolerance TestEquipment Name
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=153 WHERE ImpcCode = 'IMPC_IPG_004_001';  -- Glucose Tolerance TestEquipment Manufacturer
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=154 WHERE ImpcCode = 'IMPC_IPG_005_001';  -- Glucose Tolerance TestEquipment Model
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=155 WHERE ImpcCode = 'IMPC_IPG_006_001';  -- Glucose Tolerance TestMouse Restrained
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=156 WHERE ImpcCode = 'IMPC_IPG_007_001';  -- Glucose Tolerance TestType of Strip
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=230 WHERE ImpcCode = 'IMPC_HWT_003_001';  -- Heart WeightExperimenter
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=231 WHERE ImpcCode = 'IMPC_HWT_001_001';  -- Heart WeightDate of experiment
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=232 WHERE ImpcCode = 'IMPC_HWT_005_001';  -- Heart WeightEuthanasia
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=233 WHERE ImpcCode = 'IMPC_HWT_006_001';  -- Heart WeightEquipment name
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=234 WHERE ImpcCode = 'IMPC_HWT_010_001';  -- Heart WeightEquipment manufacturer
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=235 WHERE ImpcCode = 'IMPC_HWT_011_001';  -- Heart WeightEquipment model
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=199 WHERE ImpcCode = 'IMPC_HEM_024_001';  -- HematologyExperimenter ID
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=200 WHERE ImpcCode = 'IMPC_HEM_016_001';  -- HematologyDate and time of sacrifice 
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=201 WHERE ImpcCode = 'IMPC_HEM_015_001';  -- HematologyBlood collection tubes
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=202 WHERE ImpcCode = 'IMPC_HEM_017_001';  -- HematologyAnalyst ID
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=185 WHERE ImpcCode = 'IMPC_HEM_009_001';  -- HematologyEquipment Name
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=186 WHERE ImpcCode = 'IMPC_HEM_010_001';  -- HematologyEquipment Manufacturer
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=187 WHERE ImpcCode = 'IMPC_HEM_011_001';  -- HematologyEquipment Model
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=188 WHERE ImpcCode = 'IMPC_HEM_012_001';  -- HematologyAnethesia Used for Blood Collection
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=189 WHERE ImpcCode = 'IMPC_HEM_014_001';  -- HematologyAnticoagulant
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=193 WHERE ImpcCode = 'IMPC_HEM_018_001';  -- HematologySamples Kept on Ice Between Collection and Analysis
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=194 WHERE ImpcCode = 'IMPC_HEM_020_001';  -- HematologyID for Blood Collection SOP
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=195 WHERE ImpcCode = 'IMPC_HEM_021_001';  -- HematologyDate and Time of Blood Collection
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=197 WHERE ImpcCode = 'IMPC_HEM_013_001';  -- HematologyMethod of Blood Collection
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=198 WHERE ImpcCode = 'IMPC_HEM_026_001';  -- HematologyStorage tempature from blood collection till measurement 
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=104 WHERE ImpcCode = 'JAX_HBD_005_001';  -- HoleboardEquipment Manufacturer
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=105 WHERE ImpcCode = 'JAX_HBD_006_001';  -- HoleboardEquipment Model
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=106 WHERE ImpcCode = 'JAX_HBD_003_001';  -- HoleboardExperimenter
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=107 WHERE ImpcCode = 'JAX_HBD_007_001';  -- HoleboardStart Time
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=108 WHERE ImpcCode = 'JAX_HBD_008_001';  -- HoleboardArena ID
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=109 WHERE ImpcCode = 'JAX_HBD_009_001';  -- HoleboardArena Version
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=102 WHERE ImpcCode = 'JAX_HBD_010_001';  -- HoleboardLight Level
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=103 WHERE ImpcCode = 'JAX_HBD_004_001';  -- HoleboardEquipment Name
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=92 WHERE ImpcCode = 'JAX_LDT_013_001';  -- Light / DarkExperimenter ID
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=91 WHERE ImpcCode = 'JAX_LDT_014_001';  -- Light / DarkStart Time
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=97 WHERE ImpcCode = 'JAX_LDT_016_001';  -- Light / DarkArena Version
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=98 WHERE ImpcCode = 'JAX_LDT_017_001';  -- Light / DarkEquipment Name
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=99 WHERE ImpcCode = 'JAX_LDT_018_001';  -- Light / DarkEquipment Manufacturer
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=100 WHERE ImpcCode = 'JAX_LDT_019_001';  -- Light / DarkEquipment Model
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=93 WHERE ImpcCode = 'JAX_LDT_015_001';  -- Light / DarkArena ID
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=95 WHERE ImpcCode = 'JAX_LDT_011_001';  -- Light / DarkLight Chamber Light Level
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=96 WHERE ImpcCode = 'JAX_LDT_012_001';  -- Light / DarkDark Chamber Light Level
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=64 WHERE ImpcCode = 'JAX_OFD_039_001';  -- Open FieldConfiguration File/Software Version
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=51 WHERE ImpcCode = 'JAX_OFD_035_001';  -- Open FieldExperimenter ID
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=50 WHERE ImpcCode = 'JAX_OFD_037_001';  -- Open FieldStart time
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=62 WHERE ImpcCode = 'JAX_OFD_034_001';  -- Open FieldArena Size
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=59 WHERE ImpcCode = 'JAX_OFD_029_001';  -- Open FieldColor of Arena
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key = NULL WHERE ImpcCode = 'JAX_OFD_030_001';  -- Open FieldHeight of the Wall
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key = NULL WHERE ImpcCode = 'JAX_OFD_031_001';  -- Open FieldDistance from Light Source
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=63 WHERE ImpcCode = 'JAX_OFD_036_001';  -- Open FieldDisinfectant
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key = NULL WHERE ImpcCode = 'JAX_OFD_041_001';  -- Open FieldDate of Last Arena Calibration
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=61 WHERE ImpcCode = 'JAX_OFD_033_001';  -- Open FieldType of Analysis 
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=58 WHERE ImpcCode = 'JAX_OFD_027_001';  -- Open FieldLight Level
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key = NULL WHERE ImpcCode = 'JAX_OFD_028_001';  -- Open FieldNumber of Animals per Cage
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=57 WHERE ImpcCode = 'JAX_OFD_026_001';  -- Open FieldCentral Zone Surface Area
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=52 WHERE ImpcCode = 'JAX_OFD_038_001';  -- Open FieldArena ID
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=60 WHERE ImpcCode = 'JAX_OFD_032_001';  -- Open FieldPeriphery Zone
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=66 WHERE ImpcCode = 'JAX_OFD_051_001';  -- Open FieldResting Time Threshold
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=54 WHERE ImpcCode = 'JAX_OFD_023_001';  -- Open FieldEquipment Name
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=67 WHERE ImpcCode = 'JAX_OFD_052_001';  -- Open FieldRearing Time Threshold
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=55 WHERE ImpcCode = 'JAX_OFD_024_001';  -- Open FieldEquipment Manufacturer
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=56 WHERE ImpcCode = 'JAX_OFD_025_001';  -- Open FieldEquipment Model
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=68 WHERE ImpcCode = 'IMPC_CSD_081_001';  -- SHIRPA & DysmorphologyExperimenter
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=71 WHERE ImpcCode = 'IMPC_CSD_082_001';  -- SHIRPA & DysmorphologyLocation of test
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=72 WHERE ImpcCode = 'IMPC_CSD_083_001';  -- SHIRPA & DysmorphologyNumber of animals in cage 
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=73 WHERE ImpcCode = 'IMPC_CSD_084_001';  -- SHIRPA & DysmorphologyNumber of days since cage changed 
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=74 WHERE ImpcCode = 'IMPC_CSD_086_001';  -- SHIRPA & DysmorphologySize of squares in arena 
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=133 WHERE ImpcCode = 'IMPC_ACS_030_001';  -- Startle / PPIMouse Chamber Dimensions
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=134 WHERE ImpcCode = 'IMPC_ACS_031_001';  -- Startle / PPISound generator manufacturer
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=135 WHERE ImpcCode = 'IMPC_ACS_039_001';  -- Startle / PPISound generator model
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=115 WHERE ImpcCode = 'IMPC_ACS_014_001';  -- Startle / PPIExperimenter
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=136 WHERE ImpcCode = 'IMPC_ACS_032_001';  -- Startle / PPISound-proof box dimension
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=117 WHERE ImpcCode = 'IMPC_ACS_015_001';  -- Startle / PPIStartle Stimulus
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=137 WHERE ImpcCode = 'IMPC_ACS_038_001';  -- Startle / PPIDate Equipment last calibrated
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=118 WHERE ImpcCode = 'IMPC_ACS_013_001';  -- Startle / PPIStartle Stimulus Duration (Inter PP-S stimulus interval)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=121 WHERE ImpcCode = 'IMPC_ACS_018_001';  -- Startle / PPIPrepulse Stimulus 2
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=120 WHERE ImpcCode = 'IMPC_ACS_017_001';  -- Startle / PPIPrepulse Stimulus 1
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=122 WHERE ImpcCode = 'IMPC_ACS_019_001';  -- Startle / PPIPrepulse Stimulus 3
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=124 WHERE ImpcCode = 'IMPC_ACS_022_001';  -- Startle / PPINumber of Trials
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key = NULL WHERE ImpcCode = 'IMPC_ACS_020_001';  -- Startle / PPIPrepulse Stimulus 4
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=126 WHERE ImpcCode = 'IMPC_ACS_023_001';  -- Startle / PPIIn-chamber Adapt Time
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=138 WHERE ImpcCode = 'IMPC_ACS_026_001';  -- Startle / PPIEquipment ID
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=127 WHERE ImpcCode = 'IMPC_ACS_024_001';  -- Startle / PPIStimulus Order
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=140 WHERE ImpcCode = 'IMPC_ACS_040_001';  -- Startle / PPIAcoustic startle response measure
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=128 WHERE ImpcCode = 'IMPC_ACS_025_001';  -- Startle / PPIChamber Used
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=129 WHERE ImpcCode = 'IMPC_ACS_027_001';  -- Startle / PPIEquipment Manufacturer
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=130 WHERE ImpcCode = 'IMPC_ACS_028_001';  -- Startle / PPIEquipment Model
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=131 WHERE ImpcCode = 'IMPC_ACS_029_001';  -- Startle / PPISoftware Version
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=119 WHERE ImpcCode = 'IMPC_ACS_016_001';  -- Startle / PPIBackground
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=132 WHERE ImpcCode = 'IMPC_ACS_021_001';  -- Startle / PPIInter-trial Interval
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=116 WHERE ImpcCode = 'IMPC_ACS_011_001';  -- Startle / PPILight in Chamber
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	546	 WHERE ImpcCode = 'IMPC_ABR_004_001';  -- 	ABR - Auditory Brain Stem Response	6kHz Minimum Threshold
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	547	 WHERE ImpcCode = 'IMPC_ABR_006_001';  -- 	ABR - Auditory Brain Stem Response	12kHz Minimum Threshold
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	548	 WHERE ImpcCode = 'IMPC_ABR_008_001';  -- 	ABR - Auditory Brain Stem Response	18kHz Minimum Threshold
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	549	 WHERE ImpcCode = 'IMPC_ABR_010_001';  -- 	ABR - Auditory Brain Stem Response	24kHz Minimum Threshold
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	550	 WHERE ImpcCode = 'IMPC_ABR_012_001';  -- 	ABR - Auditory Brain Stem Response	30kHz Minimum Threshold
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	551	 WHERE ImpcCode = 'IMPC_ABR_014_001';  -- 	ABR - Auditory Brain Stem Response	PDF report
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	437	 WHERE ImpcCode = 'IMPC_DXA_006_001';  -- 	Body Composition	Subject Length
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	438	 WHERE ImpcCode = 'IMPC_DXA_001_001';  -- 	Body Composition	Subject Weight
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	446	 WHERE ImpcCode = 'IMPC_DXA_002_001';  -- 	Body Composition	Fat mass
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	447	 WHERE ImpcCode = 'IMPC_DXA_003_001';  -- 	Body Composition	Lean mass
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	448	 WHERE ImpcCode = 'IMPC_DXA_007_001';  -- 	Body Composition	BMC/ Body weight
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	449	 WHERE ImpcCode = 'IMPC_DXA_008_001';  -- 	Body Composition	Lean/ Body weight
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	450	 WHERE ImpcCode = 'IMPC_DXA_009_001';  -- 	Body Composition	Fat/ Body weight
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	451	 WHERE ImpcCode = 'IMPC_DXA_010_001';  -- 	Body Composition	Bone Area (BMC/BMD)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	440	 WHERE ImpcCode = 'IMPC_DXA_005_001';  -- 	Body Composition	BMC
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	439	 WHERE ImpcCode = 'IMPC_DXA_004_001';  -- 	Body Composition	BMD
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	209	 WHERE ImpcCode = 'IMPC_BWT_001_001';  -- 	Body Weight	Body Weight
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	210	 WHERE ImpcCode = 'IMPC_BWT_002_001';  -- 	Body Weight	Comments 
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	532	 WHERE ImpcCode = 'IMPC_CBC_013_001';  -- 	Clinical Blood Chemistry	Alanine aminotransferase  (ALT)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	528	 WHERE ImpcCode = 'IMPC_CBC_007_001';  -- 	Clinical Blood Chemistry	Albumin (ALB)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	533	 WHERE ImpcCode = 'IMPC_CBC_014_001';  -- 	Clinical Blood Chemistry	Alkaline Phosphatase
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	531	 WHERE ImpcCode = 'IMPC_CBC_012_001';  -- 	Clinical Blood Chemistry	Aspartate aminotransferase  (AST)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	538	 WHERE ImpcCode = 'IMPC_CBC_008_001';  -- 	Clinical Blood Chemistry	Bilirubin (TBIL)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	529	 WHERE ImpcCode = 'IMPC_CBC_009_001';  -- 	Clinical Blood Chemistry	Calcium (Ca)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	539	 WHERE ImpcCode = 'IMPC_CBC_005_001';  -- 	Clinical Blood Chemistry	Creatinine 
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	534	 WHERE ImpcCode = 'IMPC_CBC_018_001';  -- 	Clinical Blood Chemistry	Glucose (GLU)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	536	 WHERE ImpcCode = 'IMPC_CBC_016_001';  -- 	Clinical Blood Chemistry	HDL Cholesterol (HDLD)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	530	 WHERE ImpcCode = 'IMPC_CBC_010_001';  -- 	Clinical Blood Chemistry	Phosphorous (Phos)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	535	 WHERE ImpcCode = 'IMPC_CBC_015_001';  -- 	Clinical Blood Chemistry	Total Cholesterol (T CHOL)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	527	 WHERE ImpcCode = 'IMPC_CBC_006_001';  -- 	Clinical Blood Chemistry	Total Protein (TPROT)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	537	 WHERE ImpcCode = 'IMPC_CBC_017_001';  -- 	Clinical Blood Chemistry	Triglycerides (TG)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	526	 WHERE ImpcCode = 'IMPC_CBC_004_001';  -- 	Clinical Blood Chemistry	Urea (BUN)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	410	 WHERE ImpcCode = 'IMPC_ECG_002_001';  -- 	EKG v3	HR
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	411	 WHERE ImpcCode = 'IMPC_ECG_004_001';  -- 	EKG v3	RR
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	413	 WHERE ImpcCode = 'IMPC_ECG_006_001';  -- 	EKG v3	PR
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	414	 WHERE ImpcCode = 'IMPC_ECG_007_001';  -- 	EKG v3	QRS
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	415	 WHERE ImpcCode = 'IMPC_ECG_028_001';  -- 	EKG v3	QT
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	426	 WHERE ImpcCode = 'IMPC_ECG_001_001';  -- 	EKG v3	Number of Signals
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	427	 WHERE ImpcCode = 'IMPC_ECG_031_001';  -- 	EKG v3	Abnormal EKG Detected
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	428	 WHERE ImpcCode = 'IMPC_ECG_025_001';  -- 	EKG v3	Full Trace
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	640	 WHERE ImpcCode = 'JAX_ERG_027_001';  -- 	ERG v2.0	Comments
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	578	 WHERE ImpcCode = 'JAX_ERG_028_001';  -- 	ERG v2.0	Fundus File
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	553	 WHERE ImpcCode = 'JAX_ERG_002_001';  -- 	ERG v2.0	L-blind
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	574	 WHERE ImpcCode = 'JAX_ERG_021_001';  -- 	ERG v2.0	LE-a (ms) [Photopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	562	 WHERE ImpcCode = 'JAX_ERG_016_001';  -- 	ERG v2.0	LE-a (ms) [Scotopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	570	 WHERE ImpcCode = 'JAX_ERG_011_001';  -- 	ERG v2.0	LE-a (uV) [Photopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	561	 WHERE ImpcCode = 'JAX_ERG_006_001';  -- 	ERG v2.0	LE-a (uV) [Scotopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	575	 WHERE ImpcCode = 'JAX_ERG_022_001';  -- 	ERG v2.0	LE-b (ms) [Photopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	564	 WHERE ImpcCode = 'JAX_ERG_017_001';  -- 	ERG v2.0	LE-b (ms) [Scotopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	571	 WHERE ImpcCode = 'JAX_ERG_012_001';  -- 	ERG v2.0	LE-b (uV) [Photopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	563	 WHERE ImpcCode = 'JAX_ERG_007_001';  -- 	ERG v2.0	LE-b (uV) [Scotopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	566	 WHERE ImpcCode = 'JAX_ERG_018_001';  -- 	ERG v2.0	LE-c (ms) [Scotopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	565	 WHERE ImpcCode = 'JAX_ERG_008_001';  -- 	ERG v2.0	LE-c (uV) [Scotopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	577	 WHERE ImpcCode = 'JAX_ERG_026_001';  -- 	ERG v2.0	LE-FO-like (ms) [Scotopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	567	 WHERE ImpcCode = 'JAX_ERG_024_001';  -- 	ERG v2.0	LE-FO-like (uV) [Scotopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	552	 WHERE ImpcCode = 'JAX_ERG_001_001';  -- 	ERG v2.0	R-blind
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	572	 WHERE ImpcCode = 'JAX_ERG_019_001';  -- 	ERG v2.0	RE-a (ms) [Photopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	555	 WHERE ImpcCode = 'JAX_ERG_013_001';  -- 	ERG v2.0	RE-a (ms) [Scotopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	568	 WHERE ImpcCode = 'JAX_ERG_009_001';  -- 	ERG v2.0	RE-a (uV) [Photopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	554	 WHERE ImpcCode = 'JAX_ERG_003_001';  -- 	ERG v2.0	RE-a (uV) [Scotopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	573	 WHERE ImpcCode = 'JAX_ERG_020_001';  -- 	ERG v2.0	RE-b (ms) [Photopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	557	 WHERE ImpcCode = 'JAX_ERG_014_001';  -- 	ERG v2.0	RE-b (ms) [Scotopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	569	 WHERE ImpcCode = 'JAX_ERG_010_001';  -- 	ERG v2.0	RE-b (uV) [Photopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	556	 WHERE ImpcCode = 'JAX_ERG_004_001';  -- 	ERG v2.0	RE-b (uV) [Scotopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	559	 WHERE ImpcCode = 'JAX_ERG_015_001';  -- 	ERG v2.0	RE-c (ms) [Scotopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	558	 WHERE ImpcCode = 'JAX_ERG_005_001';  -- 	ERG v2.0	RE-c (uV) [Scotopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	576	 WHERE ImpcCode = 'JAX_ERG_025_001';  -- 	ERG v2.0	RE-FO-like (ms) [Scotopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	560	 WHERE ImpcCode = 'JAX_ERG_023_001';  -- 	ERG v2.0	RE-FO-like (uV) [Scotopic]
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	455	 WHERE ImpcCode = 'IMPC_EYE_002_001';  -- 	Eye Morphology	Bulging eye
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	460	 WHERE ImpcCode = 'IMPC_EYE_007_001';  -- 	Eye Morphology	Cornea
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	461	 WHERE ImpcCode = 'IMPC_EYE_008_001';  -- 	Eye Morphology	Cornea Opacity
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	462	 WHERE ImpcCode = 'IMPC_EYE_009_001';  -- 	Eye Morphology	Cornea vascularization
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	464	 WHERE ImpcCode = 'IMPC_EYE_081_001';  -- 	Eye Morphology	Corneal deposits
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	463	 WHERE ImpcCode = 'IMPC_EYE_080_001';  -- 	Eye Morphology	Corneal scleralization
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	454	 WHERE ImpcCode = 'IMPC_EYE_001_001';  -- 	Eye Morphology	Eye
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	458	 WHERE ImpcCode = 'IMPC_EYE_005_001';  -- 	Eye Morphology	Eye Closure
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	456	 WHERE ImpcCode = 'IMPC_EYE_003_001';  -- 	Eye Morphology	Eye Hemorrhage or Blood Presence
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	457	 WHERE ImpcCode = 'IMPC_EYE_004_001';  -- 	Eye Morphology	Eyelid morphology
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	477	 WHERE ImpcCode = 'IMPC_EYE_018_001';  -- 	Eye Morphology	Fusion between cornea and lens
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	469	 WHERE ImpcCode = 'IMPC_EYE_015_001';  -- 	Eye Morphology	Iris Pigmentation
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	468	 WHERE ImpcCode = 'IMPC_EYE_082_001';  -- 	Eye Morphology	Iris transillumination
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	470	 WHERE ImpcCode = 'IMPC_EYE_010_001';  -- 	Eye Morphology	Iris/pupil
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	475	 WHERE ImpcCode = 'IMPC_EYE_016_001';  -- 	Eye Morphology	Lens
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	476	 WHERE ImpcCode = 'IMPC_EYE_017_001';  -- 	Eye Morphology	Lens Opacity
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	459	 WHERE ImpcCode = 'IMPC_EYE_006_001';  -- 	Eye Morphology	Narrow eye opening
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	490	 WHERE ImpcCode = 'IMPC_EYE_029_001';  -- 	Eye Morphology	Ophthalmoscope Observation
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	484	 WHERE ImpcCode = 'IMPC_EYE_023_001';  -- 	Eye Morphology	Optic disc
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	488	 WHERE ImpcCode = 'IMPC_EYE_027_001';  -- 	Eye Morphology	Persistence of hyaloid vascular system
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	473	 WHERE ImpcCode = 'IMPC_EYE_013_001';  -- 	Eye Morphology	Pupil Dilation
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	474	 WHERE ImpcCode = 'IMPC_EYE_014_001';  -- 	Eye Morphology	Pupil Light Response
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	471	 WHERE ImpcCode = 'IMPC_EYE_011_001';  -- 	Eye Morphology	Pupil Position
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	472	 WHERE ImpcCode = 'IMPC_EYE_012_001';  -- 	Eye Morphology	Pupil Shape
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	481	 WHERE ImpcCode = 'IMPC_EYE_020_001';  -- 	Eye Morphology	Retina
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	485	 WHERE ImpcCode = 'IMPC_EYE_024_001';  -- 	Eye Morphology	Retinal Blood Vessels
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	487	 WHERE ImpcCode = 'IMPC_EYE_026_001';  -- 	Eye Morphology	Retinal Blood Vessels Pattern
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	486	 WHERE ImpcCode = 'IMPC_EYE_025_001';  -- 	Eye Morphology	Retinal Blood Vessels Structure
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	482	 WHERE ImpcCode = 'IMPC_EYE_021_001';  -- 	Eye Morphology	Retinal Pigmentation
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	483	 WHERE ImpcCode = 'IMPC_EYE_022_001';  -- 	Eye Morphology	Retinal Structure
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	489	 WHERE ImpcCode = 'IMPC_EYE_028_001';  -- 	Eye Morphology	Slit Lamp observation
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	491	 WHERE ImpcCode = 'IMPC_EYE_050_001';  -- 	Eye Morphology	slit or fundus photos1
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	492	 WHERE ImpcCode = 'IMPC_EYE_050_001';  -- 	Eye Morphology	slit or fundus photos2
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	493	 WHERE ImpcCode = 'IMPC_EYE_050_001';  -- 	Eye Morphology	slit or fundus photos3
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	494	 WHERE ImpcCode = 'IMPC_EYE_050_001';  -- 	Eye Morphology	slit or fundus photos4
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	495	 WHERE ImpcCode = 'IMPC_EYE_050_001';  -- 	Eye Morphology	slit or fundus photos5
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	479	 WHERE ImpcCode = 'IMPC_EYE_019_001';  -- 	Eye Morphology	Synechia
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	478	 WHERE ImpcCode = 'IMPC_EYE_083_001';  -- 	Eye Morphology	Vitreous
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	432	 WHERE ImpcCode = 'IMPC_IPG_002_001';  -- 	Glucose Tolerance Test	Plasma glucose level at Time 0
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	433	 WHERE ImpcCode = 'IMPC_IPG_002_001';  -- 	Glucose Tolerance Test	Plasma glucose level at Time 15 minutes
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	434	 WHERE ImpcCode = 'IMPC_IPG_002_001';  -- 	Glucose Tolerance Test	Plasma glucose level at Time 30 minutes
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	330	 WHERE ImpcCode = 'IMPC_GRS_001_001';  -- 	Grip Strength	Forelimb strength t1
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	331	 WHERE ImpcCode = 'IMPC_GRS_001_001';  -- 	Grip Strength	Forelimb strength t2
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	332	 WHERE ImpcCode = 'IMPC_GRS_001_001';  -- 	Grip Strength	Forelimb strength t3
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	333	 WHERE ImpcCode = 'IMPC_GRS_002_001';  -- 	Grip Strength	Fore/hind limb strength t1
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	334	 WHERE ImpcCode = 'IMPC_GRS_002_001';  -- 	Grip Strength	Fore/hind limb strength t2
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	335	 WHERE ImpcCode = 'IMPC_GRS_002_001';  -- 	Grip Strength	Fore/hind limb strength t3
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	336	 WHERE ImpcCode = 'IMPC_GRS_004_001';  -- 	Grip Strength	Other observations
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	337	 WHERE ImpcCode = 'IMPC_GRS_003_001';  -- 	Grip Strength	Weight
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	340	 WHERE ImpcCode = 'IMPC_GRS_010_001';  -- 	Grip Strength	forelimb grip mean/body weight
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	341	 WHERE ImpcCode = 'IMPC_GRS_011_001';  -- 	Grip Strength	fore and hind limb grip mean/body weight
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	338	 WHERE ImpcCode = 'IMPC_GRS_008_001';  -- 	Grip Strength	Forelimb grip mean
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	339	 WHERE ImpcCode = 'IMPC_GRS_009_001';  -- 	Grip Strength	Fore and hind limb grip mean
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	542	 WHERE ImpcCode = 'IMPC_HWT_007_001';  -- 	Heart Weight	Body Weight
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	543	 WHERE ImpcCode = 'IMPC_HWT_008_001';  -- 	Heart Weight	Heart Weight
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	496	 WHERE ImpcCode = 'IMPC_HEM_001_001';  -- 	Hematology	White Blood Cells (WBC)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	497	 WHERE ImpcCode = 'IMPC_HEM_002_001';  -- 	Hematology	Red Blood Cells (RBC)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	499	 WHERE ImpcCode = 'IMPC_HEM_004_001';  -- 	Hematology	Hematocrit (HCT)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	500	 WHERE ImpcCode = 'IMPC_HEM_005_001';  -- 	Hematology	Mean Cell Volume (MCV)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	503	 WHERE ImpcCode = 'IMPC_HEM_008_001';  -- 	Hematology	Platelet Count (PLT)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	501	 WHERE ImpcCode = 'IMPC_HEM_006_001';  -- 	Hematology	Mean corpuscular hemoglobin (CHg)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	369	 WHERE ImpcCode = 'JAX_HBD_002_001';  -- 	Holeboard	Holepoke Sequence
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	352	 WHERE ImpcCode = 'JAX_HBD_001_001';  -- 	Holeboard	Total Hole Pokes
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	NULL	 WHERE ImpcCode = 'JAX_LDT_006_001';  -- 	Light / Dark	Fecal Boli
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	345	 WHERE ImpcCode = 'JAX_LDT_003_001';  -- 	Light / Dark	Left Side Mobile Time Spent
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	344	 WHERE ImpcCode = 'JAX_LDT_002_001';  -- 	Light / Dark	Left Side Time Spent
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	350	 WHERE ImpcCode = 'JAX_LDT_010_001';  -- 	Light / Dark	No Transition
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	348	 WHERE ImpcCode = 'JAX_LDT_008_001';  -- 	Light / Dark	Pct Time in Dark
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	349	 WHERE ImpcCode = 'JAX_LDT_009_001';  -- 	Light / Dark	Pct Time in Light
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	342	 WHERE ImpcCode = 'JAX_LDT_007_001';  -- 	Light / Dark	Reaction Time
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	347	 WHERE ImpcCode = 'JAX_LDT_005_001';  -- 	Light / Dark	Right Side Mobile Time Spent
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	346	 WHERE ImpcCode = 'JAX_LDT_004_001';  -- 	Light / Dark	Right Side Time Spent
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	343	 WHERE ImpcCode = 'JAX_LDT_001_001';  -- 	Light / Dark	Side Changes
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	NULL	 WHERE ImpcCode = 'JAX_OFD_017_001';  -- 	Open Field	Center Average Speed
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	NULL	 WHERE ImpcCode = 'JAX_OFD_014_001';  -- 	Open Field	Center Distance Traveled
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	NULL	 WHERE ImpcCode = 'JAX_OFD_016_001';  -- 	Open Field	Center Permanence Time
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	NULL	 WHERE ImpcCode = 'JAX_OFD_015_001';  -- 	Open Field	Center Resting Time
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	213	 WHERE ImpcCode = 'JAX_OFD_005_001';  -- 	Open Field	Distance Traveled First Five Minutes
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	216	 WHERE ImpcCode = 'JAX_OFD_005_001';  -- 	Open Field	Distance Traveled Fourth Five Minutes
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	214	 WHERE ImpcCode = 'JAX_OFD_005_001';  -- 	Open Field	Distance Traveled Second Five Minutes
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	215	 WHERE ImpcCode = 'JAX_OFD_005_001';  -- 	Open Field	Distance Traveled Third Five Minutes
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	212	 WHERE ImpcCode = 'JAX_OFD_020_001';  -- 	Open Field	Distance Traveled Total
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	NULL	 WHERE ImpcCode = 'JAX_OFD_018_001';  -- 	Open Field	Latency to Center Entry
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	NULL	 WHERE ImpcCode = 'JAX_OFD_019_001';  -- 	Open Field	Number of Center Entries
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	221	 WHERE ImpcCode = 'JAX_OFD_006_001';  -- 	Open Field	Number of Rears First Five Minutes
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	224	 WHERE ImpcCode = 'JAX_OFD_006_001';  -- 	Open Field	Number of Rears Fourth Five Minutes
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	222	 WHERE ImpcCode = 'JAX_OFD_006_001';  -- 	Open Field	Number of Rears Second Five Minutes
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	223	 WHERE ImpcCode = 'JAX_OFD_006_001';  -- 	Open Field	Number of Rears Third Five Minutes
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	NULL	 WHERE ImpcCode = 'JAX_OFD_022_001';  -- 	Open Field	PctTime Center
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	NULL	 WHERE ImpcCode = 'JAX_OFD_013_001';  -- 	Open Field	Periphery Average Speed
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	230	 WHERE ImpcCode = 'JAX_OFD_010_001';  -- 	Open Field	Periphery Distance Traveled
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	NULL	 WHERE ImpcCode = 'JAX_OFD_012_001';  -- 	Open Field	Periphery Permanence Time
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	NULL	 WHERE ImpcCode = 'JAX_OFD_011_001';  -- 	Open Field	Periphery Resting Time
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	217	 WHERE ImpcCode = 'JAX_OFD_009_001';  -- 	Open Field	Whole Arena Average Speed
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	211	 WHERE ImpcCode = 'JAX_OFD_008_001';  -- 	Open Field	Whole Arena Permanence Time
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	218	 WHERE ImpcCode = 'JAX_OFD_007_001';  -- 	Open Field	Whole Arena Resting Time
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	263	 WHERE ImpcCode = 'IMPC_CSD_029_001';  -- 	SHIRPA & Dysmorphology	Activity (body position)
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	251	 WHERE ImpcCode = 'IMPC_CSD_079_001';  -- 	SHIRPA & Dysmorphology	Aggression
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	268	 WHERE ImpcCode = 'IMPC_CSD_007_001';  -- 	SHIRPA & Dysmorphology	Coat color - abdomen
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	269	 WHERE ImpcCode = 'IMPC_CSD_005_001';  -- 	SHIRPA & Dysmorphology	Coat color - back
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	270	 WHERE ImpcCode = 'IMPC_CSD_006_001';  -- 	SHIRPA & Dysmorphology	Coat color - head
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	271	 WHERE ImpcCode = 'IMPC_CSD_009_001';  -- 	SHIRPA & Dysmorphology	Coat color patter -abdomen
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	273	 WHERE ImpcCode = 'IMPC_CSD_010_001';  -- 	SHIRPA & Dysmorphology	Coat color patter -head
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	272	 WHERE ImpcCode = 'IMPC_CSD_008_001';  -- 	SHIRPA & Dysmorphology	Coat color pattern - back
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	277	 WHERE ImpcCode = 'IMPC_CSD_016_001';  -- 	SHIRPA & Dysmorphology	Coat hair abdomen - texture/appearance
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	278	 WHERE ImpcCode = 'IMPC_CSD_014_001';  -- 	SHIRPA & Dysmorphology	Coat hair back- texture/appearance
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	274	 WHERE ImpcCode = 'IMPC_CSD_013_001';  -- 	SHIRPA & Dysmorphology	Coat hair distribution - abdomen
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	275	 WHERE ImpcCode = 'IMPC_CSD_011_001';  -- 	SHIRPA & Dysmorphology	Coat hair distribution - back
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	276	 WHERE ImpcCode = 'IMPC_CSD_012_001';  -- 	SHIRPA & Dysmorphology	Coat hair distribution - head
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	279	 WHERE ImpcCode = 'IMPC_CSD_015_001';  -- 	SHIRPA & Dysmorphology	Coat hair head - texture/appearance
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	253	 WHERE ImpcCode = 'IMPC_CSD_077_001';  -- 	SHIRPA & Dysmorphology	Contact righting
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	316	 WHERE ImpcCode = 'IMPC_CSD_027_001';  -- 	SHIRPA & Dysmorphology	Ears
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	283	 WHERE ImpcCode = 'IMPC_CSD_044_002';  -- 	SHIRPA & Dysmorphology	Forelimb digit number
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	284	 WHERE ImpcCode = 'IMPC_CSD_048_002';  -- 	SHIRPA & Dysmorphology	Forelimb digit shape
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	285	 WHERE ImpcCode = 'IMPC_CSD_046_001';  -- 	SHIRPA & Dysmorphology	Forelimb digit size
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	286	 WHERE ImpcCode = 'IMPC_CSD_052_002';  -- 	SHIRPA & Dysmorphology	Forelimb nail length
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	287	 WHERE ImpcCode = 'IMPC_CSD_050_002';  -- 	SHIRPA & Dysmorphology	Forelimb nail number
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	288	 WHERE ImpcCode = 'IMPC_CSD_054_002';  -- 	SHIRPA & Dysmorphology	Forelimb nail shape
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	280	 WHERE ImpcCode = 'IMPC_CSD_017_001';  -- 	SHIRPA & Dysmorphology	Forelimbs - position
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	281	 WHERE ImpcCode = 'IMPC_CSD_018_001';  -- 	SHIRPA & Dysmorphology	Forelimbs - shape
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	282	 WHERE ImpcCode = 'IMPC_CSD_019_001';  -- 	SHIRPA & Dysmorphology	Forelimbs - size
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	289	 WHERE ImpcCode = 'IMPC_CSD_042_002';  -- 	SHIRPA & Dysmorphology	Forepaw shape
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	290	 WHERE ImpcCode = 'IMPC_CSD_040_002';  -- 	SHIRPA & Dysmorphology	Forepaw size
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	258	 WHERE ImpcCode = 'IMPC_CSD_033_001';  -- 	SHIRPA & Dysmorphology	Gait
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	327	 WHERE ImpcCode = 'IMPC_CSD_073_001';  -- 	SHIRPA & Dysmorphology	Genitalia morphology
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	326	 WHERE ImpcCode = 'IMPC_CSD_071_001';  -- 	SHIRPA & Dysmorphology	Genitalia presence
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	328	 WHERE ImpcCode = 'IMPC_CSD_072_001';  -- 	SHIRPA & Dysmorphology	Genitalia size
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	250	 WHERE ImpcCode = 'IMPC_CSD_080_001';  -- 	SHIRPA & Dysmorphology	Head bobbing
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	314	 WHERE ImpcCode = 'IMPC_CSD_026_001';  -- 	SHIRPA & Dysmorphology	Head morphology
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	315	 WHERE ImpcCode = 'IMPC_CSD_025_001';  -- 	SHIRPA & Dysmorphology	Head size
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	294	 WHERE ImpcCode = 'IMPC_CSD_045_002';  -- 	SHIRPA & Dysmorphology	Hindlimb digit number
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	295	 WHERE ImpcCode = 'IMPC_CSD_049_002';  -- 	SHIRPA & Dysmorphology	Hindlimb digit shape
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	296	 WHERE ImpcCode = 'IMPC_CSD_047_001';  -- 	SHIRPA & Dysmorphology	Hindlimb digit size
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	297	 WHERE ImpcCode = 'IMPC_CSD_053_002';  -- 	SHIRPA & Dysmorphology	Hindlimb nail length
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	298	 WHERE ImpcCode = 'IMPC_CSD_051_002';  -- 	SHIRPA & Dysmorphology	Hindlimb nail number
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	299	 WHERE ImpcCode = 'IMPC_CSD_055_002';  -- 	SHIRPA & Dysmorphology	Hindlimb nail shape
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	291	 WHERE ImpcCode = 'IMPC_CSD_020_001';  -- 	SHIRPA & Dysmorphology	Hindlimbs - position
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	292	 WHERE ImpcCode = 'IMPC_CSD_021_001';  -- 	SHIRPA & Dysmorphology	Hindlimbs - shape
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	293	 WHERE ImpcCode = 'IMPC_CSD_022_001';  -- 	SHIRPA & Dysmorphology	Hindlimbs - size
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	300	 WHERE ImpcCode = 'IMPC_CSD_043_002';  -- 	SHIRPA & Dysmorphology	Hindpaw shape
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	301	 WHERE ImpcCode = 'IMPC_CSD_041_002';  -- 	SHIRPA & Dysmorphology	Hindpaw size
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	247	 WHERE ImpcCode = 'IMPC_CSD_085_001';  -- 	SHIRPA & Dysmorphology	Image
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	254	 WHERE ImpcCode = 'IMPC_CSD_039_001';  -- 	SHIRPA & Dysmorphology	Limb grasp
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	259	 WHERE ImpcCode = 'IMPC_CSD_032_001';  -- 	SHIRPA & Dysmorphology	Locomotor activity
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	318	 WHERE ImpcCode = 'IMPC_CSD_076_001';  -- 	SHIRPA & Dysmorphology	Lower lip morphology
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	319	 WHERE ImpcCode = 'IMPC_CSD_070_001';  -- 	SHIRPA & Dysmorphology	Lower teeth appearance
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	317	 WHERE ImpcCode = 'IMPC_CSD_074_001';  -- 	SHIRPA & Dysmorphology	Mouth morphology
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	305	 WHERE ImpcCode = 'IMPC_CSD_060_001';  -- 	SHIRPA & Dysmorphology	Skin color - back paws
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	302	 WHERE ImpcCode = 'IMPC_CSD_058_001';  -- 	SHIRPA & Dysmorphology	Skin color - ear
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	304	 WHERE ImpcCode = 'IMPC_CSD_059_001';  -- 	SHIRPA & Dysmorphology	Skin color - front paws
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	303	 WHERE ImpcCode = 'IMPC_CSD_057_001';  -- 	SHIRPA & Dysmorphology	Skin color - snout
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	306	 WHERE ImpcCode = 'IMPC_CSD_061_001';  -- 	SHIRPA & Dysmorphology	Skin color - tail
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	307	 WHERE ImpcCode = 'IMPC_CSD_056_001';  -- 	SHIRPA & Dysmorphology	Skin color - whole body
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	311	 WHERE ImpcCode = 'IMPC_CSD_066_001';  -- 	SHIRPA & Dysmorphology	Skin texture - back paw
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	308	 WHERE ImpcCode = 'IMPC_CSD_064_001';  -- 	SHIRPA & Dysmorphology	Skin texture - ear
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	310	 WHERE ImpcCode = 'IMPC_CSD_065_001';  -- 	SHIRPA & Dysmorphology	Skin texture - front paws
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	309	 WHERE ImpcCode = 'IMPC_CSD_063_001';  -- 	SHIRPA & Dysmorphology	Skin texture - snout
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	312	 WHERE ImpcCode = 'IMPC_CSD_067_001';  -- 	SHIRPA & Dysmorphology	Skin texture - tail
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	313	 WHERE ImpcCode = 'IMPC_CSD_062_001';  -- 	SHIRPA & Dysmorphology	Skin texture - whole body
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	323	 WHERE ImpcCode = 'IMPC_CSD_028_001';  -- 	SHIRPA & Dysmorphology	Snout size
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	256	 WHERE ImpcCode = 'IMPC_CSD_036_001';  -- 	SHIRPA & Dysmorphology	Startle response
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	257	 WHERE ImpcCode = 'IMPC_CSD_034_001';  -- 	SHIRPA & Dysmorphology	Tail elevation
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	265	 WHERE ImpcCode = 'IMPC_CSD_002_001';  -- 	SHIRPA & Dysmorphology	Tail length
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	267	 WHERE ImpcCode = 'IMPC_CSD_004_001';  -- 	SHIRPA & Dysmorphology	Tail morphology
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	264	 WHERE ImpcCode = 'IMPC_CSD_001_001';  -- 	SHIRPA & Dysmorphology	Tail presence
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	266	 WHERE ImpcCode = 'IMPC_CSD_003_001';  -- 	SHIRPA & Dysmorphology	Tail thickness
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	322	 WHERE ImpcCode = 'IMPC_CSD_068_001';  -- 	SHIRPA & Dysmorphology	Teeth presence
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	260	 WHERE ImpcCode = 'IMPC_CSD_031_001';  -- 	SHIRPA & Dysmorphology	Transfer arousal
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	261	 WHERE ImpcCode = 'IMPC_CSD_030_001';  -- 	SHIRPA & Dysmorphology	Tremor
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	255	 WHERE ImpcCode = 'IMPC_CSD_038_001';  -- 	SHIRPA & Dysmorphology	Trunk curl
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	249	 WHERE ImpcCode = 'IMPC_CSD_037_001';  -- 	SHIRPA & Dysmorphology	Unexpected behaviors
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	320	 WHERE ImpcCode = 'IMPC_CSD_075_001';  -- 	SHIRPA & Dysmorphology	Upper lip morphology
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	321	 WHERE ImpcCode = 'IMPC_CSD_069_001';  -- 	SHIRPA & Dysmorphology	Upper teeth appearance
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	325	 WHERE ImpcCode = 'IMPC_CSD_024_001';  -- 	SHIRPA & Dysmorphology	Vibrissae - appearance
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	324	 WHERE ImpcCode = 'IMPC_CSD_023_001';  -- 	SHIRPA & Dysmorphology	Vibrissae - presence
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=	252	 WHERE ImpcCode = 'IMPC_CSD_078_001';  -- 	SHIRPA & Dysmorphology	Vocalization
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=377 WHERE ImpcCode = 'IMPC_ACS_033_001';  -- Startle / PPI% PPI PP1
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=378 WHERE ImpcCode = 'IMPC_ACS_034_001';  -- Startle / PPI% PPI PP2
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=379 WHERE ImpcCode = 'IMPC_ACS_035_001';  -- Startle / PPI% PPI PP3
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=371 WHERE ImpcCode = 'IMPC_ACS_001_001';  -- Startle / PPIBN 
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=372 WHERE ImpcCode = 'IMPC_ACS_002_001';  -- Startle / PPIPP1 
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=373 WHERE ImpcCode = 'IMPC_ACS_007_001';  -- Startle / PPI PP1_S
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=374 WHERE ImpcCode = 'IMPC_ACS_008_001';  -- Startle / PPI PP2_S
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=375 WHERE ImpcCode = 'IMPC_ACS_004_001';  -- Startle / PPI PP3
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=376 WHERE ImpcCode = 'IMPC_ACS_009_001';  -- Startle / PPI PP3_S
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key = NULL WHERE ImpcCode = 'IMPC_ACS_005_001';  -- Startle / PPIPP4
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key = NULL WHERE ImpcCode = 'IMPC_ACS_010_001';  -- Startle / PPIPP4_S
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), _ClimbType_key=370 WHERE ImpcCode = 'IMPC_ACS_006_001';  -- Startle / PPIS
call komp.updateDccParam(	47	,	'IMPC_GEM_061_001'	);
call komp.updateDccParam(	48	,	'IMPC_GEM_044_002'	);
call komp.updateDccParam(	49	,	'IMPC_GEM_026_002'	);
call komp.updateDccParam(	50	,	'IMPC_GEM_048_001'	);
call komp.updateDccParam(	51	,	'IMPC_GEM_062_001'	);
call komp.updateDccParam(	52	,	'IMPC_GEM_074_001'	);
call komp.updateDccParam(	53	,	'IMPC_GEM_075_001'	);
call komp.updateDccParam(	54	,	'IMPC_GEM_021_001'	);
call komp.updateDccParam(	55	,	'IMPC_GEM_076_001'	);
call komp.updateDccParam(	56	,	'IMPC_GEM_019_001'	);
call komp.updateDccParam(	639	,	'IMPC_GEM_079_001'	);
call komp.updateDccParam(	57	,	'IMPC_GEM_041_001'	);
call komp.updateDccParam(	58	,	'IMPC_GEM_063_001'	);
call komp.updateDccParam(	59	,	'IMPC_GEM_064_001'	);
call komp.updateDccParam(	60	,	'IMPC_GEM_068_001'	);
call komp.updateDccParam(	61	,	'IMPC_GEM_065_001'	);
call komp.updateDccParam(	62	,	'IMPC_GEM_066_001'	);
call komp.updateDccParam(	63	,	'IMPC_GEM_077_001'	);
call komp.updateDccParam(	64	,	'IMPC_GEM_069_001'	);
call komp.updateDccParam(	65	,	'IMPC_GEM_049_001'	);
call komp.updateDccParam(	66	,	'IMPC_GEM_067_001'	);
call komp.updateDccParam(	67	,	'IMPC_GEM_027_001'	);
call komp.updateDccParam(	68	,	'IMPC_GEM_028_001'	);
call komp.updateDccParam(	69	,	'IMPC_GEM_032_001'	);
call komp.updateDccParam(	71	,	'IMPC_GEM_043_002'	);
call komp.updateDccParam(	70	,	'IMPC_GEM_071_001'	);
call komp.updateDccParam(	72	,	'IMPC_GEM_070_001'	);
call komp.updateDccParam(	73	,	'IMPC_GEM_036_001'	);
call komp.updateDccParam(	74	,	'IMPC_GEM_033_002'	);
call komp.updateDccParam(	75	,	'IMPC_GEM_016_002'	);
call komp.updateDccParam(	76	,	'IMPC_GEM_025_002'	);
call komp.updateDccParam(	77	,	'IMPC_GEM_007_001'	);
call komp.updateDccParam(	78	,	'IMPC_GEM_078_001'	);
call komp.updateDccParam(	79	,	'IMPC_GEM_072_001'	);
call komp.updateDccParam(	80	,	'IMPC_GEM_060_001'	);
call komp.updateDccParam(	81	,	'IMPC_GEM_024_001'	);
call komp.updateDccParam(	82	,	'IMPC_GEM_047_001'	);
call komp.updateDccParam(	83	,	'IMPC_GEM_029_001'	);
call komp.updateDccParam(	84	,	'IMPC_GEM_072_001'	);
call komp.updateDccParam(	85	,	'IMPC_GEM_017_001'	);
call komp.updateDccParam(	92	,	'IMPC_GEO_062_001'	);
call komp.updateDccParam(	93	,	'IMPC_GEO_048_002'	);
call komp.updateDccParam(	94	,	'IMPC_GEO_070_001'	);
call komp.updateDccParam(	95	,	'IMPC_GEO_011_001'	);
call komp.updateDccParam(	96	,	'IMPC_GEO_018_002'	);
call komp.updateDccParam(	97	,	'IMPC_GEO_049_001'	);
call komp.updateDccParam(	98	,	'IMPC_GEO_063_001'	);
call komp.updateDccParam(	99	,	'IMPC_GEO_068_001'	);
call komp.updateDccParam(	100	,	'IMPC_GEO_069_001'	);
call komp.updateDccParam(	101	,	'IMPC_GEO_022_001'	);
call komp.updateDccParam(	102	,	'IMPC_GEO_064_001'	);
call komp.updateDccParam(	103	,	'IMPC_GEO_019_001'	);
call komp.updateDccParam(	104	,	'IMPC_GEO_041_002'	);
call komp.updateDccParam(	105	,	'IMPC_GEO_017_002'	);
call komp.updateDccParam(	106	,	'IMPC_GEO_071_001'	);
call komp.updateDccParam(	107	,	'IMPC_GEO_015_001'	);
call komp.updateDccParam(	108	,	'IMPC_GEO_016_001'	);
call komp.updateDccParam(	109	,	'IMPC_GEO_008_001'	);
call komp.updateDccParam(	110	,	'IMPC_GEO_009_002'	);
call komp.updateDccParam(	111	,	'IMPC_GEO_042_002'	);
call komp.updateDccParam(	112	,	'IMPC_GEO_050_001'	);
call komp.updateDccParam(	113	,	'IMPC_GEO_065_001'	);
call komp.updateDccParam(	114	,	'IMPC_GEO_037_001'	);
call komp.updateDccParam(	115	,	'IMPC_GEO_066_001'	);
call komp.updateDccParam(	116	,	'IMPC_GEO_047_002'	);
call komp.updateDccParam(	117	,	'IMPC_GEO_038_002'	);
call komp.updateDccParam(	118	,	'IMPC_GEO_072_001'	);
call komp.updateDccParam(	119	,	'IMPC_GEO_034_002'	);
call komp.updateDccParam(	120	,	'IMPC_GEO_061_001'	);
call komp.updateDccParam(	121	,	'IMPC_GEO_029_001'	);
call komp.updateDccParam(	122	,	'IMPC_GEO_030_001'	);
call komp.updateDccParam(	123	,	'IMPC_GEO_043_002'	);
call komp.updateDccParam(	124	,	'IMPC_GEO_067_001'	);
call komp.updateDccParam(	125	,	'IMPC_GEO_033_001'	);
call komp.updateDccParam(	126	,	'IMPC_GEO_028_001'	);
call komp.updateDccParam(	133	,	'IMPC_GEP_060_002'	);
call komp.updateDccParam(	134	,	'IMPC_GEP_087_001'	);
call komp.updateDccParam(	135	,	'IMPC_GEP_013_001'	);
call komp.updateDccParam(	136	,	'IMPC_GEP_024_001'	);
call komp.updateDccParam(	137	,	'IMPC_GEP_076_001'	);
call komp.updateDccParam(	138	,	'IMPC_GEP_063_001'	);
call komp.updateDccParam(	139	,	'IMPC_GEP_085_001'	);
call komp.updateDccParam(	140	,	'IMPC_GEP_078_001'	);
call komp.updateDccParam(	141	,	'IMPC_GEP_029_002'	);
call komp.updateDccParam(	198	,	'IMPC_GEP_086_001'	);
call komp.updateDccParam(	142	,	'IMPC_GEP_030_002'	);
call komp.updateDccParam(	143	,	'IMPC_GEP_022_001'	);
call komp.updateDccParam(	144	,	'IMPC_GEP_023_001'	);
call komp.updateDccParam(	145	,	'IMPC_GEP_047_002'	);
call komp.updateDccParam(	146	,	'IMPC_GEP_018_002'	);
call komp.updateDccParam(	147	,	'IMPC_GEP_079_001'	);
call komp.updateDccParam(	148	,	'IMPC_GEP_017_001'	);
call komp.updateDccParam(	149	,	'IMPC_GEP_061_002'	);
call komp.updateDccParam(	150	,	'IMPC_GEP_015_001'	);
call komp.updateDccParam(	151	,	'IMPC_GEP_016_001'	);
call komp.updateDccParam(	152	,	'IMPC_GEP_010_001'	);
call komp.updateDccParam(	153	,	'IMPC_GEP_011_002'	);
call komp.updateDccParam(	154	,	'IMPC_GEP_048_002'	);
call komp.updateDccParam(	155	,	'IMPC_GEP_064_001'	);
call komp.updateDccParam(	156	,	'IMPC_GEP_084_001'	);
call komp.updateDccParam(	157	,	'IMPC_GEP_042_001'	);
call komp.updateDccParam(	158	,	'IMPC_GEP_080_001'	);
call komp.updateDccParam(	159	,	'IMPC_GEP_059_002'	);
call komp.updateDccParam(	160	,	'IMPC_GEP_026_001'	);
call komp.updateDccParam(	204	,	'IMPC_GEP_081_001'	);
call komp.updateDccParam(	161	,	'IMPC_GEP_035_001'	);
call komp.updateDccParam(	162	,	'IMPC_GEP_039_002'	);
call komp.updateDccParam(	163	,	'IMPC_GEP_052_001'	);
call komp.updateDccParam(	164	,	'IMPC_GEP_005_002'	);
call komp.updateDccParam(	165	,	'IMPC_GEP_075_001'	);
call komp.updateDccParam(	166	,	'IMPC_GEP_034_001'	);
call komp.updateDccParam(	167	,	'IMPC_GEP_036_001'	);
call komp.updateDccParam(	168	,	'IMPC_GEP_049_002'	);
call komp.updateDccParam(	169	,	'IMPC_GEP_004_002'	);
call komp.updateDccParam(	170	,	'IMPC_GEP_082_001'	);
call komp.updateDccParam(	171	,	'IMPC_GEP_038_001'	);
call komp.updateDccParam(	172	,	'IMPC_GEP_083_001'	);
call komp.updateDccParam(	173	,	'IMPC_GEP_033_001'	);
call komp.updateDccParam(	8	,	'IMPC_GEL_014_001'	);
call komp.updateDccParam(	9	,	'IMPC_GEL_037_002'	);
call komp.updateDccParam(	10	,	'IMPC_GEL_024_001'	);
call komp.updateDccParam(	11	,	'IMPC_GEL_019_001'	);
call komp.updateDccParam(	12	,	'IMPC_GEL_043_001'	);
call komp.updateDccParam(	13	,	'IMPC_GEL_062_001'	);
call komp.updateDccParam(	14	,	'IMPC_GEL_063_001'	);
call komp.updateDccParam(	15	,	'IMPC_GEL_056_001'	);
call komp.updateDccParam(	16	,	'IMPC_GEL_032_001'	);
call komp.updateDccParam(	17	,	'IMPC_GEL_011_001'	);
call komp.updateDccParam(	18	,	'IMPC_GEL_028_001'	);
call komp.updateDccParam(	19	,	'IMPC_GEL_057_001'	);
call komp.updateDccParam(	20	,	'IMPC_GEL_058_001'	);
call komp.updateDccParam(	21	,	'IMPC_GEL_059_001'	);
call komp.updateDccParam(	22	,	'IMPC_GEL_030_001'	);
call komp.updateDccParam(	23	,	'IMPC_GEL_044_001'	);
call komp.updateDccParam(	24	,	'IMPC_GEL_065_001'	);
call komp.updateDccParam(	25	,	'IMPC_GEL_038_001'	);
call komp.updateDccParam(	26	,	'IMPC_GEL_029_001'	);
call komp.updateDccParam(	27	,	'IMPC_GEL_027_001'	);
call komp.updateDccParam(	28	,	'IMPC_GEL_060_001'	);
call komp.updateDccParam(	29	,	'IMPC_GEL_061_001'	);
call komp.updateDccParam(	30	,	'IMPC_GEL_042_001'	);
call komp.updateDccParam(	31	,	'IMPC_GEL_017_002'	);
call komp.updateDccParam(	32	,	'IMPC_GEL_036_002'	);
call komp.updateDccParam(	33	,	'IMPC_GEL_006_001'	);
call komp.updateDccParam(	34	,	'IMPC_GEL_055_001'	);
call komp.updateDccParam(	35	,	'IMPC_GEL_064_001'	);
call komp.updateDccParam(	37	,	'IMPC_GEL_033_001'	);
call komp.updateDccParam(	38	,	'IMPC_GEL_066_001'	);
call komp.updateDccParam(	39	,	'IMPC_GEL_018_001'	);
call komp.updateDccParam(	40	,	'IMPC_GEL_015_001'	);
call komp.updateDccParam(	182	,	'IMPC_GPM_006_001'	);
call komp.updateDccParam(	195	,	'IMPC_GPM_007_001'	);
call komp.updateDccParam(	86	,	'IMPC_GPM_018_001'	);
call komp.updateDccParam(	90	,	'IMPC_GPM_002_001'	);
call komp.updateDccParam(	87	,	'IMPC_GPM_004_001'	);
call komp.updateDccParam(	88	,	'IMPC_GPM_003_001'	);
call komp.updateDccParam(	89	,	'IMPC_GPM_001_001'	);
call komp.updateDccParam(	91	,	'IMPC_GPM_005_001'	);
call komp.updateDccParam(	194	,	'IMPC_GPP_018_001'	);
call komp.updateDccParam(	192	,	'IMPC_GPP_007_001'	);
call komp.updateDccParam(	180	,	'IMPC_GPP_006_001'	);
call komp.updateDccParam(	177	,	'IMPC_GPP_001_001'	);
call komp.updateDccParam(	175	,	'IMPC_GPP_004_001'	);
call komp.updateDccParam(	176	,	'IMPC_GPP_003_001'	);
call komp.updateDccParam(	178	,	'IMPC_GPP_002_001'	);
call komp.updateDccParam(	179	,	'IMPC_GPP_005_001'	);
call komp.updateDccParam(	196	,	'IMPC_GPL_006_001'	);
call komp.updateDccParam(	46	,	'IMPC_GPL_007_001'	);
call komp.updateDccParam(	44	,	'IMPC_GPL_002_001'	);
call komp.updateDccParam(	41	,	'IMPC_GPL_004_001'	);
call komp.updateDccParam(	42	,	'IMPC_GPL_003_001'	);
call komp.updateDccParam(	43	,	'IMPC_GPL_001_001'	);
call komp.updateDccParam(	45	,	'IMPC_GPL_005_001'	);
call komp.updateDccParam(	181	,	'IMPC_GPO_006_001'	);
call komp.updateDccParam(	193	,	'IMPC_GPO_007_001'	);
call komp.updateDccParam(	127	,	'IMPC_GPO_018_001'	);
call komp.updateDccParam(	130	,	'IMPC_GPO_001_001'	);
call komp.updateDccParam(	128	,	'IMPC_GPO_004_001'	);
call komp.updateDccParam(	129	,	'IMPC_GPO_003_001'	);
call komp.updateDccParam(	131	,	'IMPC_GPO_002_001'	);
call komp.updateDccParam(	132	,	'IMPC_GPO_005_001'	);
call komp.updateDccParam(	266	,	'IMPC_GEM_059_001'	); -- 	E12.5 Embryo Gross Morphology	Date equipment last calibrated
call komp.updateDccParam(	267	,	'IMPC_GEM_051_001'	); -- 	E12.5 Embryo Gross Morphology	Equipment ID
call komp.updateDccParam(	268	,	'IMPC_GEM_052_001'	); -- 	E12.5 Embryo Gross Morphology	Equipment Manufacturer
call komp.updateDccParam(	269	,	'IMPC_GEM_053_001'	); -- 	E12.5 Embryo Gross Morphology	Equipment Model
call komp.updateDccParam(	270	,	'IMPC_GEM_050_001'	); -- 	E12.5 Embryo Gross Morphology	Experimenter ID
call komp.updateDccParam(	271	,	'IMPC_GEM_054_001'	); -- 	E12.5 Embryo Gross Morphology	Fixative
call komp.updateDccParam(	272	,	'IMPC_GEM_056_001'	); -- 	E12.5 Embryo Gross Morphology	Somite Stage
call komp.updateDccParam(	273	,	'IMPC_GEM_058_001'	); -- 	E12.5 Embryo Gross Morphology	Time of dark cycle end
call komp.updateDccParam(	274	,	'IMPC_GEM_057_001'	); -- 	E12.5 Embryo Gross Morphology	Time of dark cycle start 
call komp.updateDccParam(	275	,	'IMPC_GEM_055_001'	); -- 	E12.5 Embryo Gross Morphology	Time of Dissection 
call komp.updateDccParam(	276	,	'IMPC_GPM_017_001'	); -- 	E12.5 Placenta Morphology	Date equipment last calibrated
call komp.updateDccParam(	277	,	'IMPC_GPM_009_001'	); -- 	E12.5 Placenta Morphology	Equipment ID
call komp.updateDccParam(	278	,	'IMPC_GPM_010_001'	); -- 	E12.5 Placenta Morphology	Equipment Manufacturer
call komp.updateDccParam(	279	,	'IMPC_GPM_011_001'	); -- 	E12.5 Placenta Morphology	Equipment Model
call komp.updateDccParam(	280	,	'IMPC_GPM_008_001'	); -- 	E12.5 Placenta Morphology	Experimenter ID
call komp.updateDccParam(	281	,	'IMPC_GPM_012_001'	); -- 	E12.5 Placenta Morphology	Fixative
call komp.updateDccParam(	282	,	'IMPC_GPM_014_001'	); -- 	E12.5 Placenta Morphology	Somite Stage
call komp.updateDccParam(	283	,	'IMPC_GPM_016_001'	); -- 	E12.5 Placenta Morphology	Time of dark cycle end
call komp.updateDccParam(	284	,	'IMPC_GPM_015_001'	); -- 	E12.5 Placenta Morphology	Time of dark cycle start 
call komp.updateDccParam(	285	,	'IMPC_GPM_013_001'	); -- 	E12.5 Placenta Morphology	Time of Dissection
call komp.updateDccParam(	286	,	'IMPC_GEO_060_001'	); -- 	E15.5 Embryo Gross Morphology	Date equipment last calibrated
call komp.updateDccParam(	287	,	'IMPC_GEO_052_001'	); -- 	E15.5 Embryo Gross Morphology	Equipment ID
call komp.updateDccParam(	288	,	'IMPC_GEO_053_001'	); -- 	E15.5 Embryo Gross Morphology	Equipment Manufacturer
call komp.updateDccParam(	289	,	'IMPC_GEO_054_001'	); -- 	E15.5 Embryo Gross Morphology	Equipment Model
call komp.updateDccParam(	290	,	'IMPC_GEO_051_001'	); -- 	E15.5 Embryo Gross Morphology	Experimenter ID
call komp.updateDccParam(	291	,	'IMPC_GEO_055_001'	); -- 	E15.5 Embryo Gross Morphology	Fixative
call komp.updateDccParam(	292	,	'IMPC_GEO_057_001'	); -- 	E15.5 Embryo Gross Morphology	Somite Stage
call komp.updateDccParam(	293	,	'IMPC_GEO_059_001'	); -- 	E15.5 Embryo Gross Morphology	Time of dark cycle end
call komp.updateDccParam(	294	,	'IMPC_GEO_058_001'	); -- 	E15.5 Embryo Gross Morphology	Time of dark cycle start 
call komp.updateDccParam(	295	,	'IMPC_GEO_056_001'	); -- 	E15.5 Embryo Gross Morphology	Time of Dissection
call komp.updateDccParam(	296	,	'IMPC_GPO_008_001'	); -- 	E15.5 Placenta Morphology	Date equipment last calibrated
call komp.updateDccParam(	297	,	'IMPC_GPO_009_001'	); -- 	E15.5 Placenta Morphology	Equipment ID
call komp.updateDccParam(	298	,	'IMPC_GPO_010_001'	); -- 	E15.5 Placenta Morphology	Equipment Manufacturer
call komp.updateDccParam(	299	,	'IMPC_GPO_011_001'	); -- 	E15.5 Placenta Morphology	Equipment Model
call komp.updateDccParam(	300	,	'IMPC_GPO_012_001'	); -- 	E15.5 Placenta Morphology	Experimenter ID
call komp.updateDccParam(	301	,	'IMPC_GPO_013_001'	); -- 	E15.5 Placenta Morphology	Fixative
call komp.updateDccParam(	302	,	'IMPC_GPO_014_001'	); -- 	E15.5 Placenta Morphology	Somite Stage
call komp.updateDccParam(	303	,	'IMPC_GPO_015_001'	); -- 	E15.5 Placenta Morphology	Time of dark cycle end
call komp.updateDccParam(	304	,	'IMPC_GPO_016_001'	); -- 	E15.5 Placenta Morphology	Time of dark cycle start
call komp.updateDccParam(	305	,	'IMPC_GPO_017_001'	); -- 	E15.5 Placenta Morphology	Time of Dissection
call komp.updateDccParam(	306	,	'IMPC_GEP_074_001'	); -- 	E18.5 Embryo Gross Morphology	Date equipment last calibrated
call komp.updateDccParam(	307	,	'IMPC_GEP_066_001'	); -- 	E18.5 Embryo Gross Morphology	Equipment ID
call komp.updateDccParam(	308	,	'IMPC_GEP_067_001'	); -- 	E18.5 Embryo Gross Morphology	Equipment Manufacturer
call komp.updateDccParam(	309	,	'IMPC_GEP_068_001'	); -- 	E18.5 Embryo Gross Morphology	Equipment Model
call komp.updateDccParam(	310	,	'IMPC_GEP_065_001'	); -- 	E18.5 Embryo Gross Morphology	Experimenter ID
call komp.updateDccParam(	311	,	'IMPC_GEP_069_001'	); -- 	E18.5 Embryo Gross Morphology	Fixative
call komp.updateDccParam(	312	,	'IMPC_GEP_071_001'	); -- 	E18.5 Embryo Gross Morphology	Somite Stage
call komp.updateDccParam(	313	,	'IMPC_GEP_073_001'	); -- 	E18.5 Embryo Gross Morphology	Time of dark cycle end
call komp.updateDccParam(	314	,	'IMPC_GEP_072_001'	); -- 	E18.5 Embryo Gross Morphology	Time of dark cycle start
call komp.updateDccParam(	315	,	'IMPC_GEP_070_001'	); -- 	E18.5 Embryo Gross Morphology	Time of Dissection
call komp.updateDccParam(	316	,	'IMPC_GPP_017_001'	); -- 	E18.5 Placenta Morphology	Date equipment last calibrated
call komp.updateDccParam(	317	,	'IMPC_GPP_009_001'	); -- 	E18.5 Placenta Morphology	Equipment ID
call komp.updateDccParam(	318	,	'IMPC_GPP_010_001'	); -- 	E18.5 Placenta Morphology	Equipment Manufacturer
call komp.updateDccParam(	319	,	'IMPC_GPP_011_001'	); -- 	E18.5 Placenta Morphology	Equipment Model
call komp.updateDccParam(	320	,	'IMPC_GPP_008_001'	); -- 	E18.5 Placenta Morphology	Experimenter ID
call komp.updateDccParam(	321	,	'IMPC_GPP_012_001'	); -- 	E18.5 Placenta Morphology	Fixative
call komp.updateDccParam(	322	,	'IMPC_GPP_014_001'	); -- 	E18.5 Placenta Morphology	Somite Stage
call komp.updateDccParam(	323	,	'IMPC_GPP_016_001'	); -- 	E18.5 Placenta Morphology	Time of dark cycle end
call komp.updateDccParam(	324	,	'IMPC_GPP_015_001'	); -- 	E18.5 Placenta Morphology	Time of dark cycle start
call komp.updateDccParam(	325	,	'IMPC_GPP_013_001'	); -- 	E18.5 Placenta Morphology	Time of Dissection
call komp.updateDccParam(	326	,	'IMPC_GEL_054_001'	); -- 	E9.5 Embryo Gross Morphology	Date equipment last calibrated
call komp.updateDccParam(	327	,	'IMPC_GEL_046_001'	); -- 	E9.5 Embryo Gross Morphology	Equipment ID
call komp.updateDccParam(	328	,	'IMPC_GEL_047_001'	); -- 	E9.5 Embryo Gross Morphology	Equipment Manufacturer
call komp.updateDccParam(	329	,	'IMPC_GEL_048_001'	); -- 	E9.5 Embryo Gross Morphology	Equipment Model
call komp.updateDccParam(	330	,	'IMPC_GEL_045_001'	); -- 	E9.5 Embryo Gross Morphology	Experimenter ID
call komp.updateDccParam(	331	,	'IMPC_GEL_049_001'	); -- 	E9.5 Embryo Gross Morphology	Fixative
call komp.updateDccParam(	332	,	'IMPC_GEL_051_001'	); -- 	E9.5 Embryo Gross Morphology	Somite Stage
call komp.updateDccParam(	333	,	'IMPC_GEL_053_001'	); -- 	E9.5 Embryo Gross Morphology	Time of dark cycle end
call komp.updateDccParam(	334	,	'IMPC_GEL_052_001'	); -- 	E9.5 Embryo Gross Morphology	Time of dark cycle start
call komp.updateDccParam(	335	,	'IMPC_GEL_050_001'	); -- 	E9.5 Embryo Gross Morphology	Time of Dissection
call komp.updateDccParam(	336	,	'IMPC_GPL_017_001'	); -- 	E9.5 Placenta Morphology	Date equipment last calibrated
call komp.updateDccParam(	337	,	'IMPC_GPL_009_001'	); -- 	E9.5 Placenta Morphology	Equipment ID
call komp.updateDccParam(	338	,	'IMPC_GPL_010_001'	); -- 	E9.5 Placenta Morphology	Equipment Manufacturer
call komp.updateDccParam(	339	,	'IMPC_GPL_011_001'	); -- 	E9.5 Placenta Morphology	Equipment Model
call komp.updateDccParam(	340	,	'IMPC_GPL_008_001'	); -- 	E9.5 Placenta Morphology	Experimenter ID
call komp.updateDccParam(	341	,	'IMPC_GPL_012_001'	); -- 	E9.5 Placenta Morphology	Fixative
call komp.updateDccParam(	342	,	'IMPC_GPL_014_001'	); -- 	E9.5 Placenta Morphology	Somite Stage
call komp.updateDccParam(	343	,	'IMPC_GPL_016_001'	); -- 	E9.5 Placenta Morphology	Time of dark cycle end
call komp.updateDccParam(	344	,	'IMPC_GPL_015_001'	); -- 	E9.5 Placenta Morphology	Time of dark cycle start
call komp.updateDccParam(	345	,	'IMPC_GPL_013_001'	); -- 	E9.5 Placenta Morphology	Time of Dissection
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), IsInput=1 WHERE _DccType_key=7;
UPDATE komp.dccparameterdetails SET ModifiedBy='michaelm', DateModified=NOW(), IsInput=0 WHERE _DccType_key<>7;

-- USERS for COLLECTED BY and Collected Date

DROP TABLE IF EXISTS `komp`.`experimenterId` ;
CREATE TABLE `komp`.`experimenterId` (
  `_experimenterId_key` int(11) NOT NULL,
  `FirstNme` varchar(128) NOT NULL,
  `LastName` varchar(128) NOT NULL,
  `IsActive` smallint(6) NOT NULL DEFAULT '1',
  `CreatedBy` varchar(128) NOT NULL DEFAULT 'dba',
  `DateCreated` datetime NOT NULL DEFAULT NOW(),
  `ModifiedBy` varchar(128) NOT NULL DEFAULT 'dba',
  `DateModified` datetime NOT NULL DEFAULT NOW(),
  `Version` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`_experimenterId_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
INSERT INTO komp.experimenterId  (FirstNme, LastName,_experimenterId_key) VALUES 
('Abigail', 'Miller', 1),
('Janet', 'Bakeman', 2),
('Mike', 'McFarland', 7),
('Seth ', 'Hannigan', 11),
('Coleen', 'Kane', 12),
('Stephen', 'Kneeland', 14),
('Alana', 'Luzzio', 15),
('Jack ', 'Marcucci', 16),
('Ben', 'Meservey', 18),
('Daniel', 'Rasicci', 24),
('Ethan', 'Saville', 25),
('Audrie', 'Seluke', 26),
('Kathy', 'Snow', 27),
('Ian', 'Welsh', 28),
('Jacqui', 'White', 29),
('Ame', 'Willett', 30),
('Jack', 'Yang', 31),
('Neil', 'Cole', 129),
('Dong', 'Nguyen-Bresinsky', 134),
('Willson', 'Roper', 136),
('Bob', 'Braun', 150),
('Kristina', 'Palmer', 210),
('Kevin', 'Peterson', 217),
('Candace', 'Bunker', 233),
('Janet', 'Bertolino', 237),
('Doug', 'Howell', 245),
('Jake', 'Lowy', 252),
('Debbie', 'Kelley', 253),
('Sierra', 'James', 266),
('Bryony', 'Hawgood', 277),
('Ais', 'Farragher-Gemma', 284),
('Brendan', 'Arbuckle', 700),
('Cynthia', 'Carpenter', 701),
('Eric', 'Bogenschutz', 704),
('Ewelina', 'Bolcun-Filas', 705),
('Charlize', 'Castro', 708),
('Jeff', 'Duryea', 709),
('Yaned', 'Gaitan', 710),
('Steve', 'Murray', 720);


DROP TABLE IF EXISTS `komp`.`submittedProcedures` ;
CREATE TABLE `komp`.`submittedProcedures` (
  `_submittedProcedures_key` int(11) NOT NULL AUTO_INCREMENT,
  `AnimalName`  varchar(64) DEFAULT NULL,
  `ExperimentName`  varchar(64) DEFAULT NULL,
  `TaskName`  varchar(64) DEFAULT NULL,
  `ImpcCode` varchar(32) DEFAULT NULL,
  `DateSubmitted` datetime,
  `XmlFilename` varchar(128),
  `Confirmed` smallint DEFAULT 0,
  `CreatedBy` varchar(128) NOT NULL DEFAULT 'dba',
  `DateCreated` datetime NOT NULL DEFAULT NOW(),
  `ModifiedBy` varchar(128) NOT NULL DEFAULT 'dba',
  `DateModified` datetime NOT NULL DEFAULT NOW(),
  `Version` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`_submittedProcedures_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `komp`.`dccQualityIssues` ;
CREATE TABLE `komp`.`dccQualityIssues` (
  `_dccQualityIssues_key` int(11) NOT NULL AUTO_INCREMENT,
  `AnimalName`  varchar(64) DEFAULT NULL,
  `TaskName`  varchar(64) DEFAULT NULL,
  `TaskInstanceKey`  int(11) DEFAULT 0,
  `ImpcCode` varchar(32) DEFAULT NULL,
  `StockNumber` varchar(16) DEFAULT NULL,
  `DateDue` datetime,
  `Issue` TEXT,
  `CreatedBy` varchar(128) NOT NULL DEFAULT 'dba',
  `DateCreated` datetime NOT NULL DEFAULT NOW(),
  `ModifiedBy` varchar(128) NOT NULL DEFAULT 'dba',
  `DateModified` datetime NOT NULL DEFAULT NOW(),
  `Version` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`_dccQualityIssues_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- KOMP CLEANUP
truncate komp.active_experiments;
truncate komp.`alz-specimen`;
truncate komp.bwtisuessuperset;
truncate komp.completed_lines_counts;
truncate komp.completenessbylines;
truncate komp.dcc_activeprocedures;
truncate komp.dcc_colonyprocedurenumbers;
truncate komp.dcc_completenessqc;
truncate komp.dcc_embryocompleteness;
truncate komp.dcc_experimentprocedures;
truncate komp.dcc_experiments_all;
truncate komp.dcc_experiments_failed;
truncate komp.dcc_failedprocedures;
truncate komp.dcc_fertilityviability;
truncate komp.dcc_lineprocedures;
truncate komp.dcc_lineqc;
truncate komp.dcc_lines_all;
truncate komp.dcc_media_dcc;
truncate komp.dcc_media_jax;
truncate komp.`dcc_rejected-mousestocknumber`;
truncate komp.dcc_specimens;
truncate komp.dcc_validprocedures;
truncate komp.dcc_xml;
truncate komp.dccalzimages;
truncate komp.dccimages;
truncate komp.dccprocedure;
truncate komp.dccqcreport;
truncate komp.dccupdates;
truncate komp.ebiimages;
truncate komp.experimenterinputs;
truncate komp.experimentsonspecimens;
truncate komp.failed;
truncate komp.failed_experiments;
truncate komp.fecal_dif_pens;
truncate komp.imagemap;
truncate komp.imagemaptmp;
truncate komp.invalidimagefilename;
truncate komp.komp_offspring_zygosities;
truncate komp.komp_task_comparisons;
truncate komp.lastbodyweight;
truncate komp.latestdccexperimentprocedures;
truncate komp.limsalzimages;
truncate komp.mating_parental_information;
truncate komp.mioutputdefn;
truncate komp.missingupdates;
truncate komp.missingupdatestmp;
truncate komp.mycompleteness;
truncate komp.nullifiedbodyweight;
truncate komp.omeroimagestagingarea;
truncate komp.openfieldsnapshot;
truncate komp.openfieldsnapshot3;
truncate komp.procedurecountsummary;
truncate komp.`qc-issues-from-dcc`;
truncate komp.qctool;
truncate komp.testtable; -- ??
truncate komp.tmpdccspecimen;
truncate komp.valid_experiments;


-- --------------------------


SELECT _ClimbType_key, COUNT(*) FROM `komp`.`dccparameterdetails` group by _ClimbType_key;
SELECT * FROM `komp`.`dccparameterdetails` where _ClimbType_key IN (92,118);
-- EAP INPUTS
SELECT 
    ProcedureDefinition, InputName, Input.ExternalID
FROM
    proceduredefinition
        INNER JOIN
    ProcedureDefinitionVersion USING (_ProcedureDefinition_key)
        INNER JOIN
    Input USING (_ProcedureDefinitionVersion_key)
WHERE
	Input.ExternalID IS NOT NULL AND CHAR_LENGTH(Input.ExternalID) > 0 AND
    _ProcedureDefinitionVersion_key IN (176 , 186,
        200,
        275,
        274,
        231,
        272,
        166,
        172,
        192,
        189,
        187,
        196,
        195,
        233,
        182,
        179);
	
-- EAP OUTPUTS
SELECT 
    ProcedureDefinition, OutputName, Output.ExternalID
FROM
    proceduredefinition
        INNER JOIN
    ProcedureDefinitionVersion USING (_ProcedureDefinition_key)
        INNER JOIN
	OutputGroup USING (_ProcedureDefinitionVersion_key)
		INNER JOIN 
	Output USING (_OutputGroup_key)
WHERE
	Output.ExternalID IS NOT NULL AND CHAR_LENGTH(Output.ExternalID) > 0 AND
    _ProcedureDefinitionVersion_key IN (176 , 186,
        200,
        275,
        274,
        231,
        272,
        166,
        172,
        192,
        189,
        187,
        196,
        195,
        233,
        182,
        179) ORDER BY ProcedureDefinition;

-- Embryo Lethal INPUTS
SELECT 
    ProcedureDefinition, InputName, Input.ExternalID
FROM
    proceduredefinition
        INNER JOIN
    ProcedureDefinitionVersion USING (_ProcedureDefinition_key)
        INNER JOIN
    Input USING (_ProcedureDefinitionVersion_key)
WHERE
    Input.ExternalID IS NOT NULL
        AND CHAR_LENGTH(Input.ExternalID) > 0
        AND _ProcedureDefinitionVersion_key IN (247 , 211, 250, 248, 267, 268, 269, 266) ORDER BY ProcedureDefinition;
	
-- Embryo Lethal OUTPUTS
SELECT 
    ProcedureDefinition, OutputName, Output.ExternalID
FROM
    proceduredefinition
        INNER JOIN
    ProcedureDefinitionVersion USING (_ProcedureDefinition_key)
        INNER JOIN
	OutputGroup USING (_ProcedureDefinitionVersion_key)
		INNER JOIN 
	Output USING (_OutputGroup_key)
WHERE
	Output.ExternalID IS NOT NULL AND CHAR_LENGTH(Output.ExternalID) > 0 AND
    _ProcedureDefinitionVersion_key IN (247 , 211, 250, 248, 267, 268, 269, 266) ORDER BY ProcedureDefinition;
	