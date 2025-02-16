## About  

This web-based system, developed as part of my graduation project, is designed for managing scientific articles, specifically to streamline and simplify the evaluation process for scientific conferences. The system, named **"ReviewHub"**, aims to improve the workflow for organizers, reviewers, and authors involved in scientific conferences.

The platform allows conference organizers to manage events, assign track managers and reviewers, and oversee the entire submission and evaluation process. For users, who can be researchers or authors, it provides a user-friendly interface to upload scientific papers, submit them for review, and track their progress through the evaluation process.

The system utilizes a variety of models to experiment with different AI functionalities to aid the authors. The **gensim** library is used for topic modeling and document similarity analysis, while **transformers** (which includes the used BERT model) enables document classification and sentiment analysis. **spaCy** is employed for natural language processing, particularly for named entity recognition, and **pyenchant** is used for spelling correction in texts.

Based on this project, my teachers and I wrote a scientific paper, which was accepted for publication at the **ICUSI 2024** (International Conference on User-System Interaction).  
You can find more details about ICUSI 2024 [here](https://rochi.utcluj.ro/icusi2024/).

The accepted papers for ICUSI 2024 can be found here: [ICUSI Proceedings](https://rochi.utcluj.ro/icusi/proceedings/current_issue.php).

## Requirements  

To run this project, you need:

- **Visual Studio Code**
- **Python < 3.9.0** (I recommend Python 3.8.10)
- **Dependencies** (install them using the command below):

```sh
pip install -r requirements.txt
```
## Demo

<div align="center">
  <img src="https://github.com/user-attachments/assets/1b9c39a9-8c0d-496f-85fb-ddc534af42af" alt="AppGif10">
  <p>Example of the user dashboard</p>
</div>

<div align="center">
  <img src="https://github.com/user-attachments/assets/808f84e2-fbf6-4189-b9e4-d71d81efc092" alt="Img1">
  <p>Example of the organizer dashboard</p>
</div>


<div align="center">
  <img src="https://github.com/user-attachments/assets/f90cd083-66d5-45e4-b68b-60239da7404e" alt="Img2">
  <p>Example of the tracker dashboard</p>
</div>


<div align="center">
  <img src="https://github.com/user-attachments/assets/59182e01-058d-4b49-8648-39ce2d868e39" alt="Img3">
  <p>Example of the reviewer dashboard</p>
</div>


<div align="center">
  <img src="https://github.com/user-attachments/assets/d57e2c34-d2f3-4615-b64f-ff581e5975bd" alt="Img4">
  <p>Example of the admin dashboard</p>
</div>

