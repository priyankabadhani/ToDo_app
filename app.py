import streamlit as st
import pandas as pd
import plotly.express as px

#database

from dp_fxns import  \
    (create_table,add_data,view_all_data,get_task,view_unique_task,edit_task_data,delete_data)

def main():
    st.title("ToDo list")

    menu = ["Create","Read","Update","Delete","About"]
    choice = st.sidebar.selectbox("Menu",menu)

    #connection
    create_table()

    if choice =="Create":
        st.subheader("Add Items")

        #layout
        col1,col2 = st.columns(2)

        with col1:
            task = st.text_area("Task To Do")

        with col2:
            task_status = st.selectbox("Status",["Todo","Doing","Done"])
            task_due_date = st.date_input("Due Date")


        #add button
        if st.button("Add Task"):
            if task:
              add_data(task,task_status,task_due_date)
              st.success("Successfully Added Data:{}".format(task))
            else:
               st.warning("Invalid Task Name")
    elif choice=="Update":
        st.subheader("Edit/Update Items")
        result = view_all_data()
        df = pd.DataFrame(result, columns=['Task', 'Status', 'Due Date'])
        with st.expander("Current Data"):
            st.dataframe(df)

        list_of_task =[i[0] for i in view_unique_task()]
        #st.write(list_of_task)
        selected_task = st.selectbox("Task To Edit",list_of_task)

        selected_result = get_task(selected_task)
        st.write(selected_result )
        if selected_result:
            task = selected_result[0][0]
            task_status = selected_result[0][1]
            task_due_date= selected_result[0][2]
            col1, col2 = st.columns(2)

            with col1:
                new_task = st.text_area("Task To Do",task)

            with col2:
                new_task_status = st.selectbox("task_status", ["ToDo", "Doing", "Done"])
                new_task_due_date = st.date_input(task_due_date)

            # add button
            if st.button("Update Task"):
                edit_task_data(new_task, new_task_status, new_task_due_date, task, task_status, task_due_date)
                st.success("Successfully Updated:: {} To::{}".format(task,new_task))

        result2 = view_all_data()
        df2 = pd.DataFrame(result2, columns=['Task', 'Status', 'Due Date'])
        with st.expander("Updated Data"):
            st.dataframe(df2)


    elif choice == "Delete":
        st.subheader("Delete Item")
        result = view_all_data()
        df = pd.DataFrame(result, columns=['Task', 'Status', 'Due Date'])
        with st.expander("Current Data"):
            st.dataframe(df)
        list_of_task = [i[0] for i in view_unique_task()]
        selected_task = st.selectbox("Task To Delete",list_of_task)
        st.warning("Do You want to Delete {}".format(selected_task))
        if st. button("Delete Task"):
            delete_data(selected_task)
            st.warning("Task Has been Successfully Deleted")


        new_result = view_all_data()
        df2 = pd.DataFrame(new_result, columns=['Task', 'Status', 'Due Date'])
        with st.expander("Updated Data"):
            st.dataframe(df2)

    elif choice == "Read":
        st.subheader("View Item")
        result = view_all_data()
        st.write(result)
        df = pd.DataFrame(result, columns=['Task', 'Status', 'Due Date'])
        with st.expander("View All Data"):
           st.dataframe(df)

        with st.expander("Task Status"):
            task_df = df['Status'].value_counts()
            task_df= task_df.reset_index()
            st.dataframe(task_df)
            p1= px.pie(task_df,names='index',values='Status')
            st.plotly_chart(p1)

    else:
        st.subheader("About")
if __name__ == '__main__':
        main()
