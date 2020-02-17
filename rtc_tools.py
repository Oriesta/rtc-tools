import numpy as np
import pandas as pd

backlog = pd.read_excel("C:\\Users\\ories\\Projects\\sample_data\\Sample Backlog.xlsx", index_col='ID')
backlog['Parent ID'].fillna(0, inplace=True)
backlog['Parent ID'] = backlog['Parent ID'].astype('int64')
backlog['Story Points'].fillna(0, inplace=True)
backlog['Story Points'] = backlog['Story Points'].astype('uint64')
backlog['Total Story Points'] = np.zeros(backlog['Story Points'].size)
backlog['Total Story Points'] = backlog['Total Story Points'].astype('uint64')
backlog['Total Points Completed'] = np.zeros(backlog['Story Points'].size)
backlog['Total Points Completed'] = backlog['Total Points Completed'].astype('uint64')

# Check if a work item has children
def hasChildren(work_item, backlog):
    
    childrenPresent = None
    
    if (backlog.loc[backlog['Parent ID'] == work_item.name]).empty:
        childrenPresent = False
    else:
        childrenPresent = True
    
    return childrenPresent

# Get all children
def getChildren(parent, backlog):

    children = backlog.loc[backlog['Parent ID'] == parent.name]
    return children

# Calculate total points (including children) for each work item
def calculateTotalPoints(work_item, backlog):
    
    id = work_item.name
    total_points = 0
    
    # Recursive criteria: parent has children
    if hasChildren(work_item, backlog) == True:
        children = getChildren(work_item, backlog)

        # Total up points from children
        for child in children.index:
            total_points += calculateTotalPoints(backlog.loc[child], backlog)

    # Base Condition: Parent has no children       
    total_points += backlog.loc[id, 'Story Points']
    backlog.loc[id, 'Total Story Points'] = total_points
    return backlog.loc[id,'Total Story Points']

'''
# Calculate total points completed (including children) for each work item
def calculateTotalPointsCompleted(parent, backlog):

    id = parent.name
    total_points = 0

    # Recursive Condition: Work item has children
    if hasChildren(parent, backlog):
        children = getChildren(parent, backlog)
        
        # Total up the points from the children
        for child in children.index:
            total_points += calculateTotalPointsCompleted(backlog.loc[child], backlog)
            
    # Base Condition: Work item is done and has no children
    if backlog.loc[id,'Status'] == 'Done':
        total_points += backlog.loc[id, 'Story Points']

    
    backlog.loc[id, 'Total Points Completed'] = total_points
    return backlog.loc[id, 'Total Points Completed']

def calculateTotalPointsByStatus(parent, backlog, status):

    id = parent.name
    total_points = 0

    # Check to see if status is valid
    status_list = backlog['Status'].unique()
    x = backlog['Status'].isin([status])
    print(x)
    return

    '''
    if backlog['Status'].isin([status]):
        print(f'Found {status} in the list status types')
        return
    else:
        print(f'Did not find {status} in the list of status types')
        return
    '''

    # Recursive condition: Work item has children
    if hasChildren(parent, backlog):
        children = getChildren(parent, backlog)

        # Total up the points from the children
        for child_index in children.index:
            total_points += calculateTotalPointsByStatus(backlog.loc[child_index], backlog, status)
    
    # Base condition: Work item has the same status as that passed in
'''

# Get all work items that don't have parents
work_items_with_no_parents = backlog.loc[backlog['Parent ID'] == 0]

# Calculate the total story points for each parent
for id in work_items_with_no_parents.index:
    backlog.loc[id, 'Total Story Points'] = calculateTotalPoints(backlog.loc[id], backlog)
    # backlog.loc[parent_id, 'Total Points Completed'] = calculateTotalPointsCompleted(backlog.loc[parent_id], backlog)
    # calculateTotalPointsByStatus(backlog.loc[parent_id], backlog, 'In Progress')


# Verify the total points are filled out for all backlog items
backlog.to_csv('Backlog_Totals.csv')