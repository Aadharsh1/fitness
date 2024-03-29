DROP DATABASE IF EXISTS workout_plans;
CREATE DATABASE workout_plans;
USE workout_plans;

CREATE TABLE workouts(
wid int(10) NOT NULL,
fitness varchar(100)	not null ,
day_number int(10)	not null,
activity  varchar(100) not null,
descrptn varchar(100),
exercise varchar(100),
no_of_sets varchar(100),

constraint workout_id primary key(wid)
);

INSERT INTO workouts (wid, fitness, day_number, activity, descrptn, exercise, no_of_sets) VALUES
(1, 'underweight', 1, 'Strength Training', NULL, 'Bench Press', '3 sets x 8-10 reps'),
(2, 'underweight', 1, 'Strength Training', NULL, 'Bicep Curls', '3 sets x 10-12 reps'),
(3, 'underweight', 1, 'Core Work', NULL, 'Plank', '3 sets x 30-60 seconds'),
(4, 'underweight', 1, 'Core Work', NULL, 'Russian Twists', '3 sets x 12-15 reps'),
(5, 'underweight', 2, 'Strength Training', NULL, 'Squats', '3 sets x 8-10 reps'),
(6, 'underweight', 2, 'Strength Training', NULL, 'Deadlifts', '3 sets x 8-10 reps'),
(7, 'underweight', 2, 'Core Work', NULL, 'Leg Raises', '3 sets x 10-12 reps'),
(8, 'underweight', 2, 'Core Work', NULL, 'Bicycle Crunches', '3 sets x 12-15 reps'),
(10, 'underweight', 3, 'Rest', 'Engage in light activity such as walking, yoga, or stretching', NULL, NULL),
(11, 'underweight', 4, 'Cardio', '5-10 minutes of light cardio', NULL, NULL),
(12, 'underweight', 4, 'Strength Training', NULL, 'Pull-ups or Assisted Pull-ups', '3 sets x 8-10 reps'),
(13, 'underweight', 4, 'Strength Training', NULL, 'Dumbbell Rows', '3 sets x 8-10 reps'),
(14, 'underweight', 4, 'Core Work', NULL, 'Plank with Leg Lifts', '3 sets x 10-12 reps'),
(15, 'underweight', 5, 'Rest', 'Complete Rest', NULL, NULL),
(16, 'underweight', 6, 'Cardio', '20-30 minutes of moderate-intensity cardio', NULL, NULL),
(17, 'underweight', 6, 'Flexibility', 'Stretching for overall flexibility and mobility', NULL, NULL),
(18, 'underweight', 7, 'Rest', 'Engage in light activity such as walking, yoga, or stretching', NULL, NULL),


(19, 'healthy', 1, 'Strength Training', NULL, 'Squats', '3 sets x 8-10 reps'),
(20, 'healthy', 1, 'Strength Training', NULL, 'Push-ups', '3 sets x 10-12 reps'),
(21, 'healthy', 1, 'Strength Training', NULL, 'Dumbbell Rows', '3 sets x 8-10 reps'),
(22, 'healthy', 1, 'Core Work', NULL, 'Plank', '3 sets x 30-60 seconds'),
(23, 'healthy', 1, 'Core Work', NULL, 'Russian Twists', '3 sets x 12-15 reps (each side)'),
(24, 'healthy', 2, 'Strength Training', NULL, 'Deadlifts', '3 sets x 8-10 reps'),
(25, 'healthy', 2, 'Strength Training', NULL, 'Bench Press', '3 sets x 8-10 reps'),
(26, 'healthy', 2, 'Strength Training', NULL, 'Pull-ups', '3 sets x 8-10 reps'),
(27, 'healthy', 2, 'Core Work', NULL, 'Leg Raises', '3 sets x 10-12 reps'),
(28, 'healthy', 2, 'Core Work', NULL, 'Bicycle Crunches', '3 sets x 12-15 reps (each side)'),
(29, 'healthy', 3, 'Rest or Light Activity', NULL, NULL, NULL),
(30, 'healthy', 4, 'Strength Training', NULL, 'Lunges', '3 sets x 10-12 reps (each leg)'),
(31, 'healthy', 4, 'Strength Training', NULL, 'Incline Bench Press', '3 sets x 8-10 reps'),
(32, 'healthy', 4, 'Strength Training', NULL, 'Lat Pulldowns', '3 sets x 8-10 reps'),
(33, 'healthy', 4, 'Core Work', NULL, 'Plank with Leg Lifts', '3 sets x 10-12 reps (each side)'),
(34, 'healthy', 4, 'Core Work', NULL, 'Reverse Crunches', '3 sets x 12-15 reps'),
(35, 'healthy', 5, 'Rest', NULL, NULL, NULL),
(36, 'healthy', 6, 'Cardio', '20-30 minutes of moderate-intensity cardio', NULL, NULL),
(37, 'healthy', 7, 'Rest or Active Recovery', NULL, NULL, NULL),



(38, 'overweight', 1, 'Strength Training', NULL, 'Bodyweight Squats', '3 sets x 10-12 reps'),
(39, 'overweight', 1, 'Strength Training', NULL, 'Incline Push-ups', '3 sets x 8-10 reps'),
(40, 'overweight', 1, 'Core Work', NULL, 'Plank', '3 sets x 30-45 seconds'),
(41, 'overweight', 1, 'Core Work', NULL, 'Standing Oblique Crunches', '3 sets x 12-15 reps (each side)'),
(42, 'overweight', 2, 'Strength Training', NULL, 'Dumbbell Shoulder Press', '3 sets x 10-12 reps'),
(43, 'overweight', 2, 'Strength Training', NULL, 'Bicep Curls', '3 sets x 10-12 reps'),
(44, 'overweight', 2, 'Core Work', NULL, 'Leg Raises', '3 sets x 10-12 reps'),
(45, 'overweight', 2, 'Core Work', NULL, 'Bicycle Crunches', '3 sets x 12-15 reps (each side)'),
(46, 'overweight', 3, 'Rest', 'Engage in light activity such as walking, yoga, or stretching', NULL, NULL),
(47, 'overweight', 4, 'Strength Training', NULL, 'Bodyweight Lunges', '3 sets x 10-12 reps (each leg)'),
(48, 'overweight', 4, 'Strength Training', NULL, 'Assisted Pull-ups', '3 sets x 8-10 reps'),
(49, 'overweight', 4, 'Core Work', NULL, 'Plank with Leg Lifts', '3 sets x 10-12 reps (each side)'),
(50, 'overweight', 4, 'Core Work', NULL, 'Reverse Crunches', '3 sets x 12-15 reps'),
(51, 'overweight', 5, 'Rest', 'Complete Rest', NULL, NULL),
(52, 'overweight', 6, 'Cardio', '20-30 minutes of low-impact cardio', NULL, NULL),
(53, 'overweight', 7, 'Rest or Active Recovery', NULL, NULL, NULL),


(54, 'obese', 1, 'Strength Training', NULL, 'Modified Push-ups (on knees)', '3 sets x 8-10 reps'),
(55, 'obese', 1, 'Strength Training', NULL, 'Lateral Arm Raises (using light dumbbells)', '3 sets x 10-12 reps'),
(56, 'obese', 1, 'Core Work', NULL, 'Seated Leg Lifts', '3 sets x 10-12 reps'),
(57, 'obese', 1, 'Core Work', NULL, 'Seated Russian Twists (using light medicine ball)', '3 sets x 12-15 reps (each side)'),
(58, 'obese', 2, 'Strength Training', NULL, 'Assisted Lat Pulldowns', '3 sets x 8-10 reps'),
(59, 'obese', 2, 'Strength Training', NULL, 'Dumbbell Shoulder Press (using light dumbbells)', '3 sets x 10-12 reps'),
(60, 'obese', 2, 'Core Work', NULL, 'Seated Leg Raises', '3 sets x 10-12 reps'),
(61, 'obese', 2, 'Core Work', NULL, 'Seated Bicycle Crunches (using light medicine ball)', '3 sets x 12-15 reps (each side)'),
(62, 'obese', 3, 'Rest or Light Activity', NULL, NULL, NULL),
(63, 'obese', 4, 'Strength Training', NULL, 'Tricep Chair Dips', '3 sets x 10-12 reps'),
(64, 'obese', 4, 'Strength Training', NULL, 'Seated Hammer Curls (using light dumbbells)', '3 sets x 10-12 reps'),
(65, 'obese', 4, 'Core Work', NULL, 'Seated Plank', '3 sets x 10-12 reps (each side)'),
(66, 'obese', 4, 'Core Work', NULL, 'Seated Reverse Crunches', '3 sets x 12-15 reps'),
(67, 'obese', 5, 'Rest', NULL, NULL, NULL),
(68, 'obese', 6, 'Cardio', '20-30 minutes of low-impact cardio', NULL, NULL),
(69, 'obese', 7, 'Rest or Active Recovery', NULL, NULL, NULL);
