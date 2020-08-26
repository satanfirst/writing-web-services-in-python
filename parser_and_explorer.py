from bs4 import BeautifulSoup


def parse(path_to_file):
    import re
    with open(path_to_file, encoding='utf-8') as fp:
        soup = BeautifulSoup(fp, 'lxml')
        body = soup.find(id='bodyContent')
        imgs, headers, linkslen, lists = 0, 0, 0, 0
        for i in body.find_all('img'):
            if int(i.get('width', 0)) >= 200:
                imgs += 1

        for i in body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            if re.search(r'^[ETC].*', i.get_text()):
                headers += 1

        res = 0
        for tag in body.find_all('a'):
            if tag.find_next_sibling() and tag.find_next_sibling().name == 'a':
                tag = tag.find_next_sibling()
                res += 1
            else:
                if tag.find_previous_sibling() and tag.find_previous_sibling().name == 'a':
                    res += 1
                if res > linkslen: linkslen = res
                res = 0

        for tag in body.find_all(['ul', 'ol']):
            if not tag.find_parents(['ul', 'ol']):
                lists += 1

    return [imgs, headers, linkslen, lists]


def valid_links_from_page(page, path, valid_pages):
    import re
    with open(f'{path}{page}', encoding='utf-8') as fp:
        links = re.findall(r'(?<=/wiki/)[\w()]+', fp.read())
        return list({a for a in links if a in valid_pages and a != page})


def bfs(graph, root, endpage):
    dist, prev = {}, {}
    dist[root] = 0
    queue = [root]
    while queue:
        curr = queue.pop(0)
        for v in graph[curr]:
            if v not in dist:
                dist[v] = dist[curr] + 1
                prev[v] = curr
                queue.append(v)
    path = []
    curr = endpage
    while curr in prev:
        path.append(curr)
        curr = prev[curr]
    return path


def build_bridge(path, start_page, end_page):
    """возвращает список страниц, по которым можно перейти по ссылкам со start_page на
    end_page, начальная и конечная страницы включаются в результирующий список"""
    import os, re
    valid_pages = os.listdir(path)
    adjacency_list, numbered_k = {}, {}
    pages = valid_links_from_page(start_page, path, valid_pages)
    numbered_k[start_page] = 0
    for i in range(len(pages)):
        numbered_k[pages[i]] = i + 1
    adjacency_list[numbered_k[start_page]] = [numbered_k[x] for x in pages]
    queue = [pages]
    visited = [start_page]
    i = len(pages)
    while queue:
        pages = queue.pop()
        for page in pages:
            if page not in visited:
                visited.append(page)
                res = valid_links_from_page(page, path, valid_pages)
                if page not in numbered_k.keys():
                    i += 1
                    numbered_k[page] = i
                if numbered_k[page] not in adjacency_list.keys():
                    for x in res:
                        if x not in numbered_k.keys():
                            i += 1
                            numbered_k[x] = i
                    adjacency_list[numbered_k[page]] = [numbered_k[x] for x in res]
                    queue.append(res)
    root = numbered_k[start_page]
    result = bfs(adjacency_list, root, numbered_k[end_page])
    return [start_page] + [k for x in result for k, v in numbered_k.items() if x == v][::-1]


def get_statistics(path, start_page, end_page):
    """собирает статистику со страниц, возвращает словарь, где ключ - название страницы,
    значение - список со статистикой страницы"""
    statistic = {}
    # получаем список страниц, с которых необходимо собрать статистику
    pages = build_bridge(path, start_page, end_page)
    for item in pages:
        statistic[item] = parse(f'{path}{item}')

    return statistic
