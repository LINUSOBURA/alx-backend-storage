-- creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student

DELIMITER //
BEGIN
	CREATE PROCEDURE ComputeAverageScoreForUser (IN user_id INT)
	AS
	select AVG(score) from corrections where corrections.user_id = user_id;
END//

DELIMITER ;
