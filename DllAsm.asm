.data

zero DD 0.0

MULTIPLIERB DD 0.114, 0.114, 0.114, 0.114
MULTIPLIERG DD 0.587, 0.587, 0.587, 0.587
MULTIPLIERR DD 0.299, 0.299, 0.299, 0.299

.code

Calculate proc
	push rbx 

	;Get and multiply the blue value by 0.114
	mov rbx, [rcx]
	movups XMM0, [rbx]
	movups XMM1, MULTIPLIERB
	pmaddwd XMM0, XMM1
	CVTTPS2DQ XMM0, XMM0

	;Get and multiply the green value by 0.587 and add it to XMM0
	mov rbx, [rcx+8]
	movups XMM2, [rbx]
	movups XMM1, MULTIPLIERG
	pmaddwd XMM2, XMM1
	CVTTPS2DQ XMM2, XMM2
	addps XMM0, XMM2

	;Get and multiply the red value by 0.299 and add it to XMM0
	mov rbx, [rcx+16]
	movups XMM2, [rbx]
	movups XMM1, MULTIPLIERR
	pmaddwd XMM2, XMM1
	CVTTPS2DQ XMM2, XMM2
	addps XMM0, XMM2

	;Return the XMM0 values to Blue array


	mov rbx, [rcx]
	movups [rbx], XMM0

	pop rbx
	ret
Calculate endp


END