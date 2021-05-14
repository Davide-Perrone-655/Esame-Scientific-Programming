'''Additional types'''

import typing as tp


#generator state typing
tpstate = tp.Optional[tp.Union[str, tp.Dict[str,tp.Union[str,tp.Dict[str,int],int]]]]

#observable function typing
tpobs = tp.Union[tp.Callable[ [tp.List[float], bool ], float ], tp.Callable[ [tp.List[float] ], float ] ]

#datas from saved observable calculation typing
tpoutdata = tp.Dict[str, tp.Union[tp.List[float],int , float, str, tp.Dict[str, tp.Dict[str, float]] ]]

#user options typing
tpopt = tp.Dict[str, tp.Optional[tp.Union[str, float, int, bool, tp.List[str]]]]