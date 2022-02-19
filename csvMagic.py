import datetime
import re
from typing import TextIO, Dict, Union, Iterable, List

RE_INT = re.compile(r"[-+]?[0-9]+$")
CellType = Union[None, int, float, str, datetime.datetime, datetime.date, datetime.time]

class CSVInvalidOptionError(Exception):
    "Bad parameters error"
    pass

class CSVMagic():
    def __init__(self, separator=',', quote_char='"', field_names: Iterable[str] = None, strict=True, has_headers=False):
        self.separator = separator
        self.quote_char = quote_char
        self.field_names : List[Union[str, int]] = list(field_names or [])
        self.strict = strict
        # Strict only allows for date entries that are of type CellType
        self.has_headers = has_headers
        
        qch = re.escape(quote_char)
        sep = re.escape(separator)
        self.re = re.compile(rf"(?:\s*)((?:{qch}(?:[^{qch}]|{qch}{qch})*{qch})|[^{sep}]*)?\s*[{sep}]?")
        
        self.first_line = True
        
        if self.field_names and has_headers:
            raise CSVInvalidOptionError("Cannot pass field_names if has_headers is True")
        
    def read(self, stream: TextIO):
        self.first_line = True
        
        for line_num, line in enumerate(stream):
            line = line.strip()
            if not line:                    # empty line
                continue
            
            parsed_line = self._parse(line_num, line)
            if self.first_line:
                self.first_line = False
                
                if self.has_headers:        # enter in the headers
                    self.field_names = [str(x) for x in parsed_line]
                    continue
                else:
                    self.field_names = list(range(len(parsed_line)))
            
            if self.strict and len(self.field_names) != len(parsed_line):
                raise ValueError(f"Line {line_num} has {len(parsed_line)} values. Expected {len(self.field_names)}")
            
            yield {x: y for x, y in zip(self.field_names, parsed_line)}
    
    def read_file(self, filename: str) -> Iterable[Dict[Union[str, int]], CellType]:
        with open(filename, "rt", encoding="utf-8") as file:
            yield from self.read(file)
            
    def _parse(self, line_num: int, line: str):
        result: List[CellType] = []
        while True:
            match = self.re_match(line)
            
            if not match:
                if self.strict:
                    raise ValueError(f"Cannot parse line {line_num}")
                else:
                    result.append(None)
                    
            result.append(self._parse_obj(line_num, match.groups()[0]))
            line = line[match.end():]
            if not match.group().endswith(self.separator):
                break
        return result          

    def is_null(self, s:str) -> bool:
        return not s.strip()
    
    def is_int(self, s:str) -> bool:
        global RE_INT
        return RE_INT.match(s) is not None
    
    def is_str(self, s:str) -> bool:
        return len(s) > 1 and s[0] == s[-1] == self.quote_char
    
    def is_date(self, s:str) ->bool:
        try:
            datetime.date.fromisoformat(s)
        except ValueError:
            return False
        return True
    
    def is_datetime(self, s:str) ->bool:
        try:
            datetime.datetime.fromisoformat(s)
        except ValueError:
            return False
        return True
    
    def is_time(self, s:str) ->bool:
        try:
            datetime.time.fromisoformat(s)
        except ValueError:
            return False
        return True
        
    def _parse_obj(self, line_num: int, block: str) -> CellType:
        
        block = block.strip()
        if self.is_null(block):
            return None
        if self.is_int(block):
            return int(block)
        if self.is_str(block):
            return str(block)
        if self.is_date(block):
            return datetime.date.fromisoformat(block)
        if self.is_datetime(block):
            return datetime.datetime.fromisoformat(block)
        if self.is_time(block):
            return datetime.time.fromisoformat(block)
        
        if self.strict:
            raise ValueError(f"Cannot parse {block} in line {line_num}")
        
        return block