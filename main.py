import sys 
from datetime import datetime
from task import Task
from storage import JSONFileStorage

def format_list(lst):
    str = ""
    for id,des,status in lst:
        str += f"{id} | {des} | {status}\n"
    return str

def main():
    if len(sys.argv)==1:
        return """
        Error : Insufficient Arguments given ,
            use one of these commands : 
            add <description> : to add new task 
            delete <id>  : to delete a task 
            update <id> : to update task 
            list : to list all tasks 
            list <todo|in-progress|done> : to see status wise task list 
            mark <todo|in-progress|done> <id> : to update status of task 
        """
    cli_args = sys.argv[1:]
    cmd = cli_args[0]
    storage = JSONFileStorage()
    match cmd:
        case "add":
            if len(cli_args)==2:
                description = cli_args[1]
                task_obj = Task(description=description)
                storage.add(task_obj)
                return f"Task Added Successfully {task_obj.id}"
            else:
                return "Invalid Format : use task-cli add <description>"
        case "delete":
            if len(cli_args)==2:
                del_id = cli_args[1]
                if storage.delete(del_id):
                    return f"Task with ID {del_id} is deleted successfully"
                return f"No Task found with ID {del_id}"
            else:
                return "Invalid Format : use task-cli delete <ID>"
        case "update":
            if len(cli_args)==3:
                update_id = cli_args[1]
                description = cli_args[2]
                update = {
                    "description": description,
                    "updateAt" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                if storage.update(update_id,update):
                    return f"Task with ID {update_id} is updated successfully"
                return f"No Task found with ID {update_id}"
            else:
                return "Invalid Format : use task-cli update <ID> <description>"
        case "list":
            if len(cli_args)==1:
                return format_list(list(map(lambda x : (x["id"],x["description"],x["status"]),storage.list())))
            elif len(cli_args)==2:
                status = cli_args[1]
                if status not in ["todo","in-progress","done"]:
                    return "Invalid status to filter tasks"
                return format_list(list(map(lambda x : (x["id"],x["description"],x["status"]),storage.list(status=status))))
            else:
                return "Invalid Format : use task-cli list <status>"

             
        case "mark":
            if len(cli_args)==3:
                update_id = cli_args[1]
                updated_status = cli_args[2]
                if updated_status not in ["todo","in-progress","done"]:
                    return "Invalid status for task"
                update = {
                    "status":updated_status,
                    "updatedAt":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                if storage.update(update_id,update):
                    return f"Task with ID {update_id}, status changed to {updated_status}"
                return f"No Task found with ID {update_id}"
            else:
                return "Invalid Format : use task-cli mark <ID> <status>"
             
        case _:
            return """ Error : Invalid command """
        
if __name__ == "__main__":
    print(main())