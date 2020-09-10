import oracle.database as db
from oracle.embeddings import get_question_embeddings

class FactBase:
    """
    Utility class for working with the KDTree and the embedding vectors database.
    A series of responses and their embeddings are stored in the responses.db file
    We use sqlite to access the database and pull the vectors.  We then store the
    vectors in a K-Dimensional Tree for efficient searching.
    """

    def __init__(self):
        self.conn, self.c = db.open_database()
        self.tree = db.database_to_tree(self.c)

    def get_best_answer(self, question, count=1):
        """
        Returns the number of best sentences, seperated by periods, given by the count variable
        """
        vec = get_question_embeddings([question,])[0]
        answers = ""
        for ans in self.tree.get_best_vectors(vec, count):
            answers += "  " + ans[1]["sentence"].rstrip()
            if answers[-1] != ".":
                answers += "."
        return answers
    
    def close(self):
        """
        Closes the database file to avoid memory leaks
        """
        db.close_database(self.c, self.conn)
