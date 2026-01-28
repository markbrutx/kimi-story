#!/usr/bin/env python3
"""
Разбивает time_traveler_novel.txt на главы для Novel Reader.
Читает файл построчно для экономии памяти.

Usage:
    cd workbench && python3 split_chapters.py
"""

import json
import re
import os
import sys
from pathlib import Path


def get_project_paths():
    """Возвращает пути относительно расположения скрипта."""
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent
    return {
        'script_dir': script_dir,
        'project_root': project_root,
        'input_file': script_dir / 'time_traveler_novel.txt',
        'output_dir': project_root / 'public' / 'chapters'
    }


def ensure_dir(path: Path) -> None:
    """Создаёт директорию если не существует."""
    path.mkdir(parents=True, exist_ok=True)


def extract_chapters(input_file: Path, output_dir: Path) -> list:
    """Разбивает файл на главы, читая построчно."""
    
    ensure_dir(output_dir)
    
    chapters = []
    current_chapter = None
    current_content = []
    chapter_num = 0
    
    # Паттерны для поиска заголовка главы в рамке
    chapter_pattern = re.compile(r'^[║]\s*ГЛАВА\s+(\d+)[:\s]+(.+?)\s*[║]')
    box_border_pattern = re.compile(r'^[╔╦═╠╬]+')
    box_bottom_pattern = re.compile(r'^[╚╩═╠╬]+')
    
    def save_current_chapter() -> None:
        """Сохраняет текущую главу в JSON."""
        nonlocal chapter_num, current_chapter, current_content
        
        if not current_chapter or not current_content:
            return
            
        # Очищаем контент
        while current_content and not current_content[0].strip():
            current_content.pop(0)
        while current_content and not current_content[-1].strip():
            current_content.pop()
        
        cleaned_content = '\n'.join(current_content)
        
        chapter_data = {
            "id": chapter_num,
            "number": current_chapter["number"],
            "title": current_chapter["title"],
            "content": cleaned_content,
            "word_count": len(cleaned_content.split()),
            "char_count": len(cleaned_content)
        }
        chapters.append(chapter_data)
        
        # Сохраняем отдельный JSON
        chapter_file = output_dir / f"chapter_{chapter_num:03d}.json"
        with open(chapter_file, 'w', encoding='utf-8') as f:
            json.dump(chapter_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Глава {chapter_num}: {current_chapter['title']} ({chapter_data['word_count']} слов)")
    
    print(f"Чтение {input_file.name} построчно...\n")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        in_chapter_box = False
        expect_title = False
        
        for line in f:
            line_stripped = line.rstrip()
            
            # Начало рамки главы
            if box_border_pattern.match(line_stripped) and not in_chapter_box:
                expect_title = True
                continue
            
            # Заголовок главы внутри рамки
            if expect_title:
                match = chapter_pattern.match(line_stripped)
                if match:
                    save_current_chapter()
                    
                    chapter_num += 1
                    current_chapter = {
                        "number": int(match.group(1)),
                        "title": match.group(2).strip()
                    }
                    current_content = []
                    in_chapter_box = True
                expect_title = False
                continue
            
            # Конец рамки главы
            if in_chapter_box and box_bottom_pattern.match(line_stripped):
                in_chapter_box = False
                continue
            
            # Пропускаем технические строки
            if in_chapter_box or expect_title:
                continue
            
            # Собираем контент главы
            if current_chapter is not None:
                current_content.append(line.rstrip('\n'))
    
    # Сохраняем последнюю главу
    save_current_chapter()
    
    # Создаём индекс
    index = {
        "total_chapters": len(chapters),
        "chapters": [
            {"id": c["id"], "number": c["number"], "title": c["title"], "word_count": c["word_count"]} 
            for c in chapters
        ]
    }
    
    with open(output_dir / "index.json", 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Готово! Разбито на {len(chapters)} глав.")
    print(f"📁 Данные сохранены в: {output_dir}")
    
    return chapters


def main() -> int:
    """Entry point."""
    paths = get_project_paths()
    
    if not paths['input_file'].exists():
        print(f"❌ Файл не найден: {paths['input_file']}")
        print("Убедитесь, что time_traveler_novel.txt находится в папке workbench/")
        return 1
    
    extract_chapters(paths['input_file'], paths['output_dir'])
    return 0


if __name__ == "__main__":
    sys.exit(main())
