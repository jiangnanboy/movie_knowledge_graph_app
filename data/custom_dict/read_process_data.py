import os



actor_path = os.path.join(os.getcwd(), '演员名.txt')
actor_process_path = os.path.join(os.getcwd(), '演员名p.txt')
actor_process_dict_path = os.path.join(os.getcwd(), '演员名dict.txt')

movie_path = os.path.join(os.getcwd(), '电影名.txt')
movie_process_path = os.path.join(os.getcwd(), '电影名p.txt')
movie_process_dict_path = os.path.join(os.getcwd(), '电影名dict.txt')


with open(actor_path, 'r', encoding='utf-8') as actor_read, open(actor_process_path, 'w', encoding='utf-8') as actor_write, open(actor_process_dict_path, 'w', encoding='utf-8') as actor_dict_write:
    for line in actor_read:
        line = line.strip()
        line_pro = line.lower()
        line_pro = ''.join(line_pro.split())

        actor_write.write(line_pro)
        actor_write.write('\n')

        actor_dict_write.write(line + '#' + line_pro)
        actor_dict_write.write('\n')



with open(movie_path, 'r', encoding='utf-8') as movie_read, open(movie_process_path, 'w', encoding='utf-8') as movie_write, open(movie_process_dict_path, 'w', encoding='utf-8') as movie_dict_write:
    for line in movie_read:
        line = line.strip()
        line_pro = line.lower()
        line_pro = ''.join(line_pro.split())

        movie_write.write(line_pro)
        movie_write.write('\n')

        movie_dict_write.write(line + '#' + line_pro)
        movie_dict_write.write('\n')