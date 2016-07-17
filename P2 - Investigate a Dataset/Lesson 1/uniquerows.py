import unicodecsv

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

enrollments = read_csv('/datasets/ud170/udacity-students/enrollments.csv')
daily_engagement = read_csv('/datasets/ud170/udacity-students/daily_engagement.csv')
project_submissions = read_csv('/datasets/ud170/udacity-students/project_submissions.csv')
    
### For each of these three tables, find the number of rows in the table and
### the number of unique students in the table. To find the number of unique
### students, you might want to create a set of the account keys in each table.

def uniquerows(data, key):
    unique_rows = set()
    for d in data:
        unique_rows.add(d[key])
    print len(unique_rows)

enrollment_num_rows = len(enrollments) 
enrollment_num_unique_students = uniquerows(enrollments, 'account_key')

engagement_num_rows = len(daily_engagement)
engagement_num_unique_students = uniquerows(daily_engagement, 'acct')

submission_num_rows = len(project_submissions)
submission_num_unique_students = uniquerows(project_submissions, 'account_key')