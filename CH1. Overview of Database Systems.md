# CH1. Overview of Database Systems

- 基本名詞解釋
    - A **database** is a collection of data, typically describing the activities of one or more related organizations.
    - A **database management system**, or DBMS, is software designed to assist in maintaining and utilizing large collections of data.
    - A **data model** is a collection of concepts for describing data.
        
        一組用來描述資料庫結構概念集合，以及資料庫應該要遵守的某些限制。
        
    - A **schema** is a description of a particular collection of data, using the a given data model.
    - A **transaction** is an atomic sequence of database actions (reads/writes).
- 使用DBMS的好處
    1. Data independence 資料獨立性
        
        > Database application programs are independent of the details of data representation and storage.
        > 
    2. Efficient access 易於存取
        
        > DBMS provides efficient storage and retrieval mechanisms, including support for very large files, index structures and query optimization.
        > 
    3. Reduced application development time 減少開發時間
        
        > Since the DBMS provides several important functions required by applications, only application-specific code needs to be written.
        > 
    4. **Data integrity 資料完整性**
        
        > Is normally enforced in a database system by a series of integrity constraints or rules.
        > 
        1. ***Entity integrity*** concerns the concept of a [primary key](https://en.wikipedia.org/wiki/Primary_key), which the column or columns chosen to be the primary key should be **unique** and **not null**.
        2. ***Referential integrity*** concerns the concept of a [foreign key](https://en.wikipedia.org/wiki/Foreign_key). 
        3. ***Domain integrity*** specifies that all columns in a relational database must be declared upon a defined domain.
        4. ***User-defined integrity*** refers to a set of rules specified by a user, which do not belong to the entity, domain and referential integrity categories.
    5. Security 資料安全性
        
        > Can enforce access contmls that govern what data is visible to different classes of users.
        > 
    6. Uniform data administration 資料管理
        
        > When several users share the data, centralizing the administration of data can offer significant improvements.
        > 
    7. Concurrent Access 可多人同時存取
    8. Crash Recovery 資料復原
- 資料庫架構與資料獨立性
    <img width="984" alt="Untitled" src="https://github.com/pei9564/advanced-database-management/assets/103319735/89612a8d-5d77-4143-afab-29cbc7442a2b">
    1. 外部架構（external schema）
    2. 概念架構（conceptual schema）⇒ 邏輯資料獨立性（可以只改表格架構）
    3. 內部架構（internal schema）⇒ 實體資料獨立性（可以只改程式）
- 使用資料庫的可能會遇到的問題
    1. 交錯動作（Interleaving actions）
引發的不連續性（inconsistency）
    2. 資料庫當機（crush）引發的動作不完整
    3. 資料庫彼此等待的死結（Deadlock）
- 問題解決方法－資料庫演算法
    1. 原子性（Atomicity）
        1. 資料庫的一筆交易中的動作，不是全部成功就是全部失敗(all-or-nothing property)
        2. 若欲當機或死結 → 報廢交易（Aborted）並全部重新執行
    2. 鎖定狀態（Phase Lock）
        1. 二元鎖定：lock、unlock
        2. 共享/互斥鎖定：read_lock(Share-locked)、write_lock(Exclusive-locked)、unlock
            ⇒ S→S（可）、S→X（不可）、X→S（不可）ㄒ、X→X（不可）
        3. 嚴格型鎖定（strict 2PL）：交易完成之前，其他交易都不能存取該交易的項目
    3. 預寫日誌記錄（Write ahead logging, WAL protocol）
        1. 在資料庫動作前先寫下紀錄(log)
        2. 記錄包含：原始值、更改值、交易狀態（undo, redo, etc.）
