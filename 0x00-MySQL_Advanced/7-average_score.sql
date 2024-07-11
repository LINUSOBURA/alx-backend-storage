-- creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student


CREATE TABLE IF NOT EXISTS user_avarages (
		user_id INT PRIMARY KEY,
			average_score DECIMAL(10, 2)
			)

			DELIMITER //

			CREATE PROCEDURE ComputeAverageScoreForUser (IN user_id INT)

			BEGIN
				DECLARE avg_score DECIMAL(10, 2);

				select AVG(score) INTO avg_score from corrections where user_id = user_id;

				INSERT INTO user_avarages ( user_id, average_score ) VALUES(
						 user_id, avg_score)
						 ON DUPLICATE KEY UPDATE average_score = avg_score;

					END//

					DELIMITER ;

