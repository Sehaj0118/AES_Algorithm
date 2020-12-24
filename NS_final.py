import numpy as np
from pyfinite import ffield
import copy

def round_keys_generation(initial_key, total_rounds):
	######### part of standard algorithm

	round_keys_arr = [] ## array which holds 11 keys
	key = initial_key	## inital key
	round_keys_arr.append(key) ## first key is the initial key
	i=0
	while(i<total_rounds):
		w0,w1,w2,w3 = key[0],key[1],key[2],key[3]
		
		## 1-byte left rotation 
		w4 = [w3[1], w3[2], w3[3], w3[0]]

		temp = []
		j=0
		while(j<len(w4)):
			## doing look_up using 8 bits from S_box and also coverting hexadecimal to integer!!
			val = SBOX[int(w4[j][0],16)][int(w4[j][1],16)]
			temp.append(val)
			j+=1
		w4=temp
		# w4=substitute_word(w4)
		num=16
		w4 = finding_xor(w4, [RC_BOX[i],'00','00','00'],num)
		# print("helooooooooooooooooooooooo")
		# print(w4)
		# print()
		w4 = finding_xor(w4, w0,num)
		
		w5 = finding_xor(w4, w1,num)
		
		w6 = finding_xor(w5, w2,num)
		
		w7= finding_xor(w6, w3,num)
		key = [w4, w5, w6, w7]
		round_keys_arr.append(key)
		i+=1
	return round_keys_arr

def finding_xor(x1,x2,num):
	arr = []
	i=0
	while(i<len(x1)):
		num1,num2 = x1[i],x2[i]
		arr.append("".join(["%x" % (int(y,num) ^ int(z,num)) for (y, z) in zip(num1, num2)]).upper())
		i+=1
	return arr


def Add_Round_Key(st_matrix,round_key):
	matrix = []
	i=0
	while(i<len(st_matrix)):
		word = st_matrix[i] ## retreiving the ith 4-bytes array of state matrix
		key = round_key[i]  ## retreiving the ith 4-bytes array of round key matrix
		matrix.append(finding_xor(word,key,16)) ## finding xor and keeping the result
		i+=1 
	return matrix

def Subtitute_bytes(st_matrix,decider):
	i=0
	matrix=[]
	size = len(st_matrix)
	while(i<size):
		word = st_matrix[0] ## taking out the 1st 4-bytes array every time 
		del st_matrix[0]
		temp = []
		j=0
		## same as substitute word
		while(j<len(word)):
			if(decider==0):
				## doing look_up using 8 bits from SBOX and also coverting hexadecimal to integer!!
				val = SBOX[int(word[j][0],16)][int(word[j][1],16)]
			else:
				## doing look_up using 8 bits from INV_SBOX and also coverting hexadecimal to integer!!
				val = INV_SBOX[int(word[j][0],16)][int(word[j][1],16)]
			temp.append(val)
			j+=1
		matrix.append(temp)
		i+=1
	return matrix

def Shift_Row(st_matrix):
	state_matrix = np.array(st_matrix).T.tolist() ## taking transpose of state matrix
	matrix = []
	matrix.append(state_matrix[0]) ## left shifting by 0-bytes i.e., doing nothing
	del state_matrix[0]
	
	word=state_matrix[0]  ## extracting 2nd row
	del state_matrix[0]  
	a = word[0]		## left shifting by 1 byte but using "del" keyword
	del word[0]
	word.append(a) 
	matrix.append(word)

	word=state_matrix[0] ## extracting 3nd row
	del state_matrix[0]  ## left shifting by 2 bytes but using "del" keyword
	a=word[0]
	del word[0]
	word.append(a)
	a=word[0]
	del word[0]
	word.append(a)
	matrix.append(word)
	
	word=state_matrix[0]  ## extracting 4th row
	del state_matrix[0]		## left shifting by 3 bytes but using "del" keyword
	a=word[0]
	del word[0]
	word.append(a)
	a=word[0]
	del word[0]
	word.append(a)
	a=word[0]
	del word[0]
	word.append(a)
	matrix.append(word)

	matrix = np.array(matrix).T.tolist() ## converting again to the same state	
	return matrix

def Shift_Row_Inverse (state_matrix):
	state_matrix = np.array(st_matrix).T.tolist() ## taking transpose of state matrix
	matrix = []
	
	matrix.append(state_matrix[0]) ## left shifting by 0-bytes i.e., doing nothing
	del state_matrix[0]

	word=state_matrix[0]  ## extracting 1st row
	del state_matrix[0]		## left shifting by 3 bytes but using "del" keyword
	a=word[0]
	del word[0]
	word.append(a)
	a=word[0]
	del word[0]
	word.append(a)
	a=word[0]
	del word[0]
	word.append(a)
	matrix.append(word)

	word=state_matrix[0] ## extracting 2nd row
	del state_matrix[0]  ## left shifting by 2 bytes but using "del" keyword
	a=word[0]
	del word[0]
	word.append(a)
	a=word[0]
	del word[0]
	word.append(a)
	matrix.append(word)

	word=state_matrix[0]  ## extracting 3rd row
	del state_matrix[0]  
	a = word[0]		## left shifting by 1 byte but using "del" keyword
	del word[0]
	word.append(a) 
	matrix.append(word)
	
	matrix = np.array(matrix).T.tolist() ## converting again to the same state	
	return matrix

def Mix_Column(st_matrix,MC_matrix,MC_matrix_Inverse,decider):
	state_matrix = np.array(st_matrix).T.tolist() ## taking transpose of state matrix to present it in column wise
	column = [""]*4
	i=0
	while(i<4):
		j=0
		while(j<4):
			column[j] = state_matrix[j][i]	## iterating through coloumn
			j+=1

		## converting to int from hexadecimal
		for k in range(len(column)):
			column[k]=int(column[k],16)

		## performing multiplication in galois field
		helping_arr = copy.deepcopy(column) ## using helping array to retrieve the old values of column
		f = ffield.FField(8,gen=0x11b,useLUT=0)	
		## multiplication of 1st column
		if(decider==0):	## normal mix column takes place then
			column[0] = f.Multiply(helping_arr[0], MC_matrix[0][0]) ^ f.Multiply(helping_arr[1], MC_matrix[0][1]) ^ f.Multiply(helping_arr[2], MC_matrix[0][2]) ^ f.Multiply(helping_arr[3], MC_matrix[0][3])	
			column[1] = f.Multiply(helping_arr[0], MC_matrix[1][0]) ^ f.Multiply(helping_arr[1], MC_matrix[1][1]) ^ f.Multiply(helping_arr[2], MC_matrix[1][2]) ^ f.Multiply(helping_arr[3], MC_matrix[1][3])
			column[2] = f.Multiply(helping_arr[0], MC_matrix[2][0]) ^ f.Multiply(helping_arr[1], MC_matrix[2][1]) ^ f.Multiply(helping_arr[2], MC_matrix[2][2]) ^ f.Multiply(helping_arr[3], MC_matrix[2][3])
			column[3] = f.Multiply(helping_arr[0], MC_matrix[3][0]) ^ f.Multiply(helping_arr[1], MC_matrix[3][1]) ^ f.Multiply(helping_arr[2], MC_matrix[3][2]) ^ f.Multiply(helping_arr[3], MC_matrix[3][3])
		else:
			column[0] = f.Multiply(helping_arr[0], MC_matrix_Inverse[0][0]) ^ f.Multiply(helping_arr[1], MC_matrix_Inverse[0][1]) ^ f.Multiply(helping_arr[2], MC_matrix_Inverse[0][2]) ^ f.Multiply(helping_arr[3], MC_matrix_Inverse[0][3])	
			column[1] = f.Multiply(helping_arr[0], MC_matrix_Inverse[1][0]) ^ f.Multiply(helping_arr[1], MC_matrix_Inverse[1][1]) ^ f.Multiply(helping_arr[2], MC_matrix_Inverse[1][2]) ^ f.Multiply(helping_arr[3], MC_matrix_Inverse[1][3])
			column[2] = f.Multiply(helping_arr[0], MC_matrix_Inverse[2][0]) ^ f.Multiply(helping_arr[1], MC_matrix_Inverse[2][1]) ^ f.Multiply(helping_arr[2], MC_matrix_Inverse[2][2]) ^ f.Multiply(helping_arr[3], MC_matrix_Inverse[2][3])
			column[3] = f.Multiply(helping_arr[0], MC_matrix_Inverse[3][0]) ^ f.Multiply(helping_arr[1], MC_matrix_Inverse[3][1]) ^ f.Multiply(helping_arr[2], MC_matrix_Inverse[3][2]) ^ f.Multiply(helping_arr[3], MC_matrix_Inverse[3][3])
		## converting again to hexadecimal
		column[0] = format(column[0],'X')
		column[1] = format(column[1],'X')
		column[2] = format(column[2],'X')
		column[3] = format(column[3],'X')

		## inserting '0' in the front to make the hexadecimal of 8 bit
		if(len(column[0])==1):
			column[0] = '0'+column[0]
		if(len(column[1])==1):
			column[1] = '0'+column[1]
		if(len(column[2])==1):
			column[2] = '0'+column[2]
		if(len(column[3])==1):
			column[3] = '0'+column[3]						

		## assigning new state_matrix column
		j=0
		while(j<4):
			state_matrix[j][i] = column[j]
			j+=1
		i+=1
	state_matrix = np.array(state_matrix).T.tolist() ## taking transpose of state matrix to present it in row wise again
	return state_matrix

if __name__=="__main__":

	## taking plain text as input that needs to be encrypted
	pl_text = input("Input Plaintext:") 
	## taking 16 bytes key which is used for encryption
	key = input("Input 16 byte key for encrypting the plaintext:")
	pl_text_bytes = [] ## plain_text's hexa bytes for each character
	key_bytes=[] ## key's hexa bytes for each character	
	print("\n \n")
	i=0
	while(i<len(pl_text)):
		## converting plaintext's character to hexa decimal
		pl_text_bytes.append(format(ord(pl_text[i]),'X'))
		i+=1
	# print("Plaintext after conversion: ",pl_text_bytes)
	# print()


	i=0
	while(i<len(key)):
		## converting key's character to hexa decimal
		key_bytes.append(format(ord(key[i]),'X'))
		i+=1
	# print("Key after conversion: ",key_bytes)
	# print()

	## making plaintext_bytes into blocks of 16 bytes
	num=16
	val=(num-(len(pl_text_bytes)%num))%num ## outside mod operation is handling the case when the plaintext is of multiple of 16 bytes
	
	i=0
	while(i<val):
		## appending the val for the remaining bytes values 
		pl_text_bytes.append('0'+format(val,'X'))
		i+=1
	# print("16 byte blocks of plaintext: ",pl_text_bytes)
	# print("Number of plaintext blocks: ",int(len(pl_text_bytes)/num))
	# print()

	a=4 ## using for 4bytes array
	pl_text_block_bytes = []	## storing the (4 array of 4 bytes) as a single row 
	small_arr_bytes = []	## 4 bytes array
	large_arr_bytes = []	## 16 bytes array
	j=0
	while(j<len(pl_text_bytes)):
		small_arr_bytes.append(pl_text_bytes[j])
		if((j+1)%a==0):
			## inserting 4 bytes array into 16 bytes array 
			large_arr_bytes.append(small_arr_bytes)
			## cleaning 4 bytes array
			small_arr_bytes=[]
		if((j+1)%num==0):
			## inserting 16 bytes array into pl_text_block_bytes array
			pl_text_block_bytes.append(large_arr_bytes)
			## cleaning 16 bytes array
			large_arr_bytes=[]
		j+=1

	print("plaintext in blocks of bytes:\n",pl_text_block_bytes)
	print()

	key_block_bytes = [] ## storing the 4 bytes as a single row
	small_arr_bytes=[]	## 4 bytes array
	j=0
	while(j<len(key_bytes)):
		small_arr_bytes.append(key_bytes[j])
		if((j+1)%a==0):
			## inserting 4 bytes into key_block_bytes array
			key_block_bytes.append(small_arr_bytes)
			small_arr_bytes=[]
		j+=1
	print("key in blocks of bytes: \n",key_block_bytes)
	# print()	

	print("Keys Generation process initiating...")


	INV_SBOX = [['52', '09', '6A', 'D5', '30', '36', 'A5', '38', 'BF', '40', 'A3', '9E', '81', 'F3', 'D7', 'FB'],
	['7C', 'E3', '39', '82', '9B', '2F', 'FF', '87', '34', '8E', '43', '44', 'C4', 'DE', 'E9', 'CB'],
	['54', '7B', '94', '32', 'A6', 'C2', '23', '3D', 'EE', '4C', '95', '0B', '42', 'FA', 'C3', '4E'],
	['08', '2E', 'A1', '66', '28', 'D9', '24', 'B2', '76', '5B', 'A2', '49', '6D', '8B', 'D1', '25'],
	['72', 'F8', 'F6', '64', '86', '68', '98', '16', 'D4', 'A4', '5C', 'CC', '5D', '65', 'B6', '92'],
	['6C', '70', '48', '50', 'FD', 'ED', 'B9', 'DA', '5E', '15', '46', '57', 'A7', '8D', '9D', '84'],
	['90', 'D8', 'AB', '00', '8C', 'BC', 'D3', '0A', 'F7', 'E4', '58', '05', 'B8', 'B3', '45', '06'],
	['D0', '2C', '1E', '8F', 'CA', '3F', '0F', '02', 'C1', 'AF', 'BD', '03', '01', '13', '8A', '6B'],
	['3A', '91', '11', '41', '4F', '67', 'DC', 'EA', '97', 'F2', 'CF', 'CE', 'F0', 'B4', 'E6', '73'],
	['96', 'AC', '74', '22', 'E7', 'AD', '35', '85', 'E2', 'F9', '37', 'E8', '1C', '75', 'DF', '6E'],
	['47', 'F1', '1A', '71', '1D', '29', 'C5', '89', '6F', 'B7', '62', '0E', 'AA', '18', 'BE', '1B'],
	['FC', '56', '3E', '4B', 'C6', 'D2', '79', '20', '9A', 'DB', 'C0', 'FE', '78', 'CD', '5A', 'F4'],
	['1F', 'DD', 'A8', '33', '88', '07', 'C7', '31', 'B1', '12', '10', '59', '27', '80', 'EC', '5F'],
	['60', '51', '7F', 'A9', '19', 'B5', '4A', '0D', '2D', 'E5', '7A', '9F', '93', 'C9', '9C', 'EF'],
	['A0', 'E0', '3B', '4D', 'AE', '2A', 'F5', 'B0', 'C8', 'EB', 'BB', '3C', '83', '53', '99', '61'],
	['17', '2B', '04', '7E', 'BA', '77', 'D6', '26', 'E1', '69', '14', '63', '55', '21', '0C', '7D']]

	RC_BOX = ['01','02','04','08','10','20','40','80','1B','36']

	SBOX = [['63', '7C', '77', '7B', 'F2', '6B', '6F', 'C5', '30', '01', '67', '2B', 'FE', 'D7', 'AB', '76' ],
	['CA', '82', 'C9', '7D', 'FA', '59', '47', 'F0', 'AD', 'D4', 'A2', 'AF', '9C', 'A4', '72', 'C0'],
	['B7', 'FD', '93', '26', '36', '3F', 'F7', 'CC', '34', 'A5', 'E5', 'F1', '71', 'D8', '31', '15'],
	['04', 'C7', '23', 'C3', '18', '96', '05', '9A', '07', '12', '80', 'E2', 'EB', '27', 'B2', '75'],
	['09', '83', '2C', '1A', '1B', '6E', '5A', 'A0', '52', '3B', 'D6', 'B3', '29', 'E3', '2F', '84'],
	['53', 'D1', '00', 'ED', '20', 'FC', 'B1', '5B', '6A', 'CB', 'BE', '39', '4A', '4C', '58', 'CF'],
	['D0', 'EF', 'AA', 'FB', '43', '4D', '33', '85', '45', 'F9', '02', '7F', '50', '3C', '9F', 'A8'],
	['51', 'A3', '40', '8F', '92', '9D', '38', 'F5', 'BC', 'B6', 'DA', '21', '10', 'FF', 'F3', 'D2'],
	['CD', '0C', '13', 'EC', '5F', '97', '44', '17', 'C4', 'A7', '7E', '3D', '64', '5D', '19', '73'],
	['60', '81', '4F', 'DC', '22', '2A', '90', '88', '46', 'EE', 'B8', '14', 'DE', '5E', '0B', 'DB'],
	['E0', '32', '3A', '0A', '49', '06', '24', '5C', 'C2', 'D3', 'AC', '62', '91', '95', 'E4', '79'],
	['E7', 'C8', '37', '6D', '8D', 'D5', '4E', 'A9', '6C', '56', 'F4', 'EA', '65', '7A', 'AE', '08'],
	['BA', '78', '25', '2E', '1C', 'A6', 'B4', 'C6', 'E8', 'DD', '74', '1F', '4B', 'BD', '8B', '8A'],
	['70', '3E', 'B5', '66', '48', '03', 'F6', '0E', '61', '35', '57', 'B9', '86', 'C1', '1D', '9E'],
	['E1', 'F8', '98', '11', '69', 'D9', '8E', '94', '9B', '1E', '87', 'E9', 'CE', '55', '28', 'DF'],
	['8C', 'A1', '89', '0D', 'BF', 'E6', '42', '68', '41', '99', '2D', '0F', 'B0', '54', 'BB', '16']]

	MC_matrix = [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]
	MC_matrix_Inverse=[[14,11,13,9],[9,14,11,13],[13,9,14,11],[11,13,9,14]]

	round_keys_arr = round_keys_generation(key_block_bytes, 10)
	tillnow = ""
	for x in range(len(round_keys_arr)):
		tillnow+= str(round_keys_arr[x]) + "\n"
	print("11 roundkeys are:\n", tillnow)
	print("Key generation completed.")
	print()


	print("starting encryption")
	size = int(len(pl_text_bytes)/16) ## size of plain_text_byte
	cypher_text = ""

	i=0
	cypher_block_bytes=[]
	while(i<size):
		# print("block encoding ",i+1)
		st_matrix = pl_text_block_bytes[0] ## making state matrix of first 16 bytes block

		tillNow=""
		for x in range(len(st_matrix)):
			tillNow+= str(st_matrix[x]) + " "

		print("plain text before initial permutation of encryption: \n" + tillNow )

		del pl_text_block_bytes[0]
		# print("Adding round key 0 ")
		st_matrix = Add_Round_Key(st_matrix,round_keys_arr[0]) ## performing initial permutation with 0th key
		# print(st_matrix)
		# print()
		
		tillNow=""
		for x in range(len(st_matrix)):
			tillNow+= str(st_matrix[x]) + " "
		print("Plain text after initial permutation of encryption: \n" + tillNow)

		j=0
		while(j<9):

			# print("Subtitute round ",j+1)
			st_matrix=Subtitute_bytes(st_matrix,0)
			# print(st_matrix)
			# print()
			# print("Shift round ", j+1)
			st_matrix=Shift_Row(st_matrix)
			# print(st_matrix)
			# print()
			# print("Mix columns round ", j+1)
			st_matrix=Mix_Column(st_matrix,MC_matrix,MC_matrix_Inverse,0)
			# print(st_matrix)
			# print()
			# print("Add round key ", j+1)
			st_matrix=Add_Round_Key(st_matrix, round_keys_arr[j+1])
			# print(st_matrix)
			# print()
			# pl_text_block_bytes.append(st_matrix) ## appending to the pl_text_block_bytes

			tillNow=""
			for x in range(len(st_matrix)):
				tillNow+= str(st_matrix[x]) + " "	
			print("Plain text after round " + str(j+1) + " :\n" + tillNow )


			j+=1
		# print("Substitute round 10")
		st_matrix=Subtitute_bytes(st_matrix,0)
		# print(st_matrix)
		# print()
		# print("Shift row round 10")
		st_matrix=Shift_Row(st_matrix)
		# print()
		# print(st_matrix)
		# print("Add round key 10")
		st_matrix = Add_Round_Key(st_matrix, round_keys_arr[10])
		# print(st_matrix)
		cypher_block_bytes.append(st_matrix)
		# print()

		tillNow=""
		for x in range(len(st_matrix)):
			tillNow+= str(st_matrix[x]) + " "	
		
		print("Plaintext after round 10 (special) :\n" + tillNow)

	
		j=0
		while(j<4):
			k=0
			while(k<4):
				cypher_text+=st_matrix[j][k]
				k+=1
			j+=1
		i+=1
		# print("Cyphertext until now: ", cypher_text)
		# print()

	print("The final cyphertext is: ", cypher_text + " \n")

	print("Decrypting the cypher text: ")
	cypher_to_plain_text=""
	i=0
	while(i<size):
		# print("block decoding ",i+1)

		tillNow=""
		for x in range(len(st_matrix)):
			tillNow+= str(st_matrix[x]) + " "
		
		print("Cipher text before first (special) round of decryption: \n" + tillNow)

		st_matrix = cypher_block_bytes[0] ## making state matrix of first 16 bytes block
		del cypher_block_bytes[0]
		# print("Adding round key 10 ")
		st_matrix = Add_Round_Key(st_matrix,round_keys_arr[10]) ## 
		# print(st_matrix)
		# print()
		# print("Inverse Shift round ", 10)
		st_matrix=Shift_Row_Inverse(st_matrix)
		# print(st_matrix)
		# print()
		# print("Inverse Subtitute round ",10)
		st_matrix=Subtitute_bytes(st_matrix,1)
		# print(st_matrix)
		# print()
		tillNow=""
		for x in range(len(st_matrix)):
			tillNow+= str(st_matrix[x]) + " "

		print("Cipher text after first round of decryption: \n" + tillNow )

		j=0
		while(j<9):
			# print("Add round key ", 9-j)
			st_matrix=Add_Round_Key(st_matrix, round_keys_arr[9-j])
			# print(st_matrix)
			# print()

			# print("Inverse Mix columns round ", 9-j)
			st_matrix=Mix_Column(st_matrix,MC_matrix,MC_matrix_Inverse,1)
			# print(st_matrix)
			# print()

			# print("Inverse Shift round ", 9-j)
			st_matrix=Shift_Row_Inverse(st_matrix)
			# print(st_matrix)
			# print()

			# print("Inverse Subtitute round ",9-j)
			st_matrix=Subtitute_bytes(st_matrix,1)
			# print(st_matrix)
			# print()

			# pl_text_block_bytes.append(st_matrix) ## appending to the pl_text_block_bytes

			tillNow=""
			for x in range(len(st_matrix)):
				tillNow+= str(st_matrix[x]) + " "
			print("Cypher text after round " + str(j+2) + " :\n" + tillNow)

			j+=1

		# print("Add round key 0")
		st_matrix = Add_Round_Key(st_matrix, round_keys_arr[0])
		# print(st_matrix)
		pl_text_block_bytes.append(st_matrix)
		# print()

		tillNow=""
		for x in range(len(st_matrix)):
			tillNow+= str(st_matrix[x]) + " "	

		print("Cipher text after final permutation round (adding original key) :\n" + tillNow)

		j=0
		while(j<4):
			k=0
			while(k<4):
				cypher_to_plain_text+=st_matrix[j][k]
				k+=1
			j+=1
		i+=1
		# print("Cypher to plain text until now: ", cypher_to_plain_text)
		# print()

	print("Full deciphered (Hex) message: ",cypher_to_plain_text + "\n")
	# str = unicode(cypher_to_plain_text, errors='replace')
	print("Finally Cypher to plain text (Readable): ", bytes.fromhex(cypher_to_plain_text).decode('utf-8'))

# We have successfully implemented AES for our Network Security Assignment 2