class refund_data:
    def __init__(self , category):
        category_condition = trimmed_df['category_title'] == category
        self.category_df = trimmed_df[category_condition] #생성자
        
    def sub_category(self, sub_title): #변수에 서브 카테고리 타이틀
        category_df = self.category_df
        sub_mask = category_df['subcategory_title'] == sub_title
        return category_df[sub_mask] #서브카테고리만 슬라이싱해서 리턴
    
    def refund(self,sub_title):
        sub_df = self.sub_category(sub_title)
        refund_check_cond = sub_df['type'] == 'REFUND' #REFUND 찾는 조건식
        return sub_df[refund_check_cond]
	 #서브 카테고리에서 타입이 REFUND인 자료 모두 리턴 , 환불전체 건수를 알 수 있다.
    
    def refund_amount_print(self,sub_title): #환불건수 프린트하는 메소드
        refund_sub_df = self.refund(sub_title)
        print(len(refund_sub_df)) 
    
    def refund_plus(self,sub_title):
        sub_df = self.sub_category(sub_title) #서브카테고리 전체 자료
        refund_sub_df = self.refund(sub_title) #타입이 REFUND인 자료
        id_check_cond_refund = sub_df['customer_id'].isin(list(refund_sub_df['customer_id']))
	 #환불한 id에 속하는지 확인하는 조건, 이번기 구매도 같이 한 건수를 찾기 위함
        return sub_df[id_check_cond_refund].sort_values(by=["customer_id"], ascending=[True])
	 #환불을 한 번이라도 한 자료를 구했음 (이번기 환불만 or 이번기 구매+환불) #id로 정렬해서 묶었음.
    
    def refund_plus_amount_print(self, sub_title): #환불을 한 번이라도 한 건수프린트하는 메소드
        sub_df_sorted = self.refund_plus(sub_title)
        print(len(sub_df_sorted))

    def pair_refund(self, sub_title): #PAYMENT , REFUND 짝이 맞는 자료를 구하는 메소드
        sub_df_sorted = self.refund_plus(sub_title)
        return sub_df_sorted[sub_df_sorted['type'] == 'PAYMENT']

    def pair_refund_print(self, sub_title): #PAYMENT , REFUND 짝이 맞는 건수를 출력하는 메소드
        sub_df_sorted = self.refund_plus(sub_title)
        print(len(sub_df_sorted[sub_df_sorted['type'] == 'PAYMENT'])) 

    def refund_ratio(self, sub_title): #환불율을 구하는 메소드
        sub_df = self.sub_category(sub_title)
        refund_sub_df = self.refund(sub_title)
        refund_plus_df = self.refund_plus(sub_title)
        refund_pair_df = self.pair_refund(sub_title)
        only_refund = len(refund_plus_df) - 2*len(refund_pair_df)
	 #오직 이번기간에 환불한 건수를 구했다. #한 번이라도 환불한 건수 - payment,refund 쌍을 뺌
        refund_ratio = round((len(refund_sub_df) - only_refund) / (len(sub_df) - only_refund) *100 , 2)
	        #환불율을 구하면 >> 분모에는 (전체 데이터 분석 거래수 - 이번기에 구매 안 하고 환부란 한 거래 건수) 
	,분자에는 (전체 환불 거래수 - 이번기에 구매 안 하고 환부란 한 거래 건수)
        return refund_ratio
