import whatthepatch
import os
import click

def is_nochange(change):
    if type(change.old) == int and type(change.new) == int:
        return True
    return False
def is_deletions(change):
    if type(change.old) == int and change.new is None:
        return True
    return False
def extract_lines(changes):
    func_stack = []
    pairs = []
    for i in changes:
        if is_nochange(i) is False:
            func_stack.append(i)
        if len(func_stack) > 0 and is_nochange(i) is True:
            inserts = []
            deletions = []
            while len(func_stack) > 0:
                item = func_stack.pop()
                item_str = item.line.strip()
                if is_deletions(item): 
                    deletions.append(item_str)
                else: 
                    inserts.append(item_str)
            deletions.reverse()
            inserts.reverse()
            pairs.append((deletions, inserts))
            func_stack = []
    return pairs

def dump_data(change_pairs, single_line_path, multi_line_path):
    deletions = change_pairs[0]
    inserts = change_pairs[1]
    deletions_item = len(deletions)
    inserts_item = len(inserts)
    
    s_bugy_file = os.path.join(single_line_path, 'sing_bugy.txt')
    s_fix_file = os.path.join(single_line_path, 'sing_fix.txt')
    
    m_bugy_file = os.path.join(multi_line_path, 'mul_bugy.txt')
    m_fix_file = os.path.join(multi_line_path, 'mul_fix.txt')
    
    if deletions_item == inserts_item and 0 < inserts_item < 2 and len(deletions[0]) != 0:
        with open(s_bugy_file, "a+") as f:
            f.write(f'{deletions[0]}\n')
        with open(s_fix_file, "a+") as f:
            f.write(f'{inserts[0]}\n')
    else:
        with open(m_bugy_file, "a+") as f:
            f.write('### bugy ###:\n')
            for i in deletions:
                f.write(f'{i}\n')
        with open(m_fix_file, "a+") as f:
            f.write('### fix  ###:\n')
            for i in inserts:
                f.write(f'{i}\n')

@click.command()
@click.option('--diff_src')
@click.option('--single_desc')
@click.option('--multi_desc')
def handle_diffs(diff_src, single_desc, multi_desc):
    with open(diff_src) as f:
        text = f.read()
    diff = [x for x in whatthepatch.parse_patch(text)]
    for i in diff:
        rr = extract_lines(i.changes)
        for j in rr:
            dump_data(j, single_desc, multi_desc)

if __name__ == '__main__':
    handle_diffs()