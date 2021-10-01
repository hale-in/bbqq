import torch.nn
from typing import List, Tuple
from transformers import BertTokenizer, BertModel
from torch.nn import functional as F

DATA: List[Tuple[str, int]] = [
    ("김 총리 “현행 거리두기 2주 연장…사적모임제한 유지”", 0),
    ("靑 \"日총리 취임후 정상 통화 검토\"…정상회담 재추진 계기 주목", 0),
    ("\"커피만 팔았을 뿐인데\"… 모호한 규정속 애타는 '커피숍'", 1),
    ("[스트레이트 예고] 당첨자 명단 단독 입수 \"엘시티, 빈 칸 세대의 비밀\"", 2)
]

class BBQQClassifer(torch.nn.Module):
    def __init__(self, bert: BertModel):
        self.bert = bert
        self.linear = torch.nn.Linear()

    def forward(self):
        pass

    def training_step(self):
        pass


def main():
    model = BertModel.from_pretrained("monologg/kobert")
    tokenizer = BertTokenizer.from_pretrained("monologg/kobert")
    X = tokenizer([sent for sent, _ in DATA],
                  padding=True,
                  truncation=True,
                  return_tensors='pt')
    y = torch.LongTensor([label for _, label in DATA])
    Out = model(**X)
    H_all = Out['last_hidden_state'] #cls-김-총리-.. (L, H)
    print(H_all.shape)
    H_cls = H_all[: , 0]  # (N, L, H) -> (N, H)
    W = torch.nn.Linear(H_all.shape[2], 3) #클래스
    Scores = W(H_cls)  # (N, H) * (H, 3) -> (N, 3)
    Scores = torch.softmax(Scores, dim=1)
    print(Scores)
    loss = F.cross_entropy(Scores, y)
    print(loss)
    clssifier = BBQQClassifer()
    optimizer = clssifier.parameters()

if __name__ == '__main__':
    main()