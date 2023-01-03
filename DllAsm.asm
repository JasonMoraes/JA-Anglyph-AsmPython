.data

zero DD 0.0
twelve DD 12.0
;[red, green, blue, red, green, blue, red, green, blue, red, green, blue]

MULTIPLIERB DD 0.114, 0.114, 0.114, 0.114
MULTIPLIERG DD 0.587, 0.587, 0.587, 0.587
MULTIPLIERR DD 0.299, 0.299, 0.299, 0.299

.code

Calculate proc
	push rbx 
	mov rbx, rcx ; get address of array
    mov eax, 0
    xorps xmm3, xmm3 ;set all xmm to all 0s, absolute must have
    xorps xmm1, xmm1
    xorps xmm2, xmm2

    ; loop through array of pointers and extract items
    mov rcx, 0              ; initialize loop counter

    loop_start:
        shufps xmm1, xmm1, 93h ;rotate left the register
        mov rax, rcx
        imul rax, 12 ;each pixel contains 12 bytes, so multiply index by 12
        mov edx, [rbx + rax] ;1st value
        movd xmm4, edx   ;transfer data to xmm1 register using helper xmm4
        paddd xmm1, xmm4

        shufps xmm2, xmm2, 93h ;rotate left the register
        mov rax, rcx
        imul rax, 12 ;each pixel contains 12 bytes
        mov edx, [rbx + rax + 4] ;2nd value
        movd xmm4, edx   
        paddd xmm2, xmm4

        shufps xmm3, xmm3, 93h
        mov rax, rcx
        imul rax, 12 ;each pixel contains 12 bytes
        mov edx, [rbx + rax + 8] ;3rd value
        movd xmm4, edx
        paddd xmm3, xmm4           ; move value to xmm - not the cleanest way, but working
        inc rcx                    ; increment loop counter
        cmp rcx, 4                 ; check if ecx is equal to 4 - repeat for each of 4 pixels
    jne loop_start             ; jump to loop_start if ecx is not equal to 4

    
    movups xmm4, MULTIPLIERB ;multiply using monochromatic anagliph alghoritm values
    mulps xmm1, xmm4
    movups xmm4, MULTIPLIERG
    mulps xmm2, xmm4
    movups xmm4, MULTIPLIERR
    mulps xmm3, xmm4
    
    addpd xmm3, xmm2 ; sum the red color using alghoritm
    paddd xmm3, xmm1
    
    
    ;save red values - could be in loop
    movd eax, xmm3
    mov [rbx +44], eax
    shufps xmm3, xmm3, 39h
    movd eax, xmm3
    mov [rbx + 32], eax
    shufps xmm3, xmm3, 39h
    movd eax, xmm3
    mov [rbx + 20], eax
    shufps xmm3, xmm3, 39h
    movd eax, xmm3
    mov [rbx + 8], eax



    add rbx, 48 ;jump to right image pixels
    mov rcx, 0 ;reset loop counter
    xorps xmm3, xmm3 ;set all xmm to all 0s, absolute must have
    xorps xmm1, xmm1
    xorps xmm2, xmm2

    loop_start2: ;loop for second part of image
       shufps xmm1, xmm1, 93h ;rotate left the register
        mov rax, rcx
        imul rax, 12 ;each pixel contains 12 bytes, so multiply index by 12
        mov edx, [rbx + rax] ;1st value
        movd xmm4, edx   ;transfer data to xmm1 register using helper xmm4
        paddd xmm1, xmm4

        shufps xmm2, xmm2, 93h ;rotate left the register
        mov rax, rcx
        imul rax, 12 ;each pixel contains 12 bytes
        mov edx, [rbx + rax + 4] ;2nd value
        movd xmm4, edx   
        paddd xmm2, xmm4

        shufps xmm3, xmm3, 93h
        mov rax, rcx
        imul rax, 12 ;each pixel contains 12 bytes
        mov edx, [rbx + rax + 8] ;3rd value
        movd xmm4, edx
        paddd xmm3, xmm4           ; move value to xmm - not the cleanest way, but working
        inc rcx                    ; increment loop counter
        cmp rcx, 4                 ; check if ecx is equal to 4 - repeat for each of 4 pixels
    jne loop_start2           ; jump to loop_start if ecx is not equal to 4

    sub rbx, 48 ; return to beggining of array
    movups xmm4, MULTIPLIERB
    mulps xmm1, xmm4
    movups xmm4, MULTIPLIERG
    mulps xmm2, xmm4
    movups xmm4, MULTIPLIERR
    mulps xmm3, xmm4
    
    addpd xmm1, xmm2 ; sum the green and blue colors using alghoritm
    paddd xmm1, xmm3

    movups xmm2, xmm1 ; copy the value for green color


     ; save green
    movd eax, xmm2
    mov [rbx +40], eax
    shufps xmm2, xmm2, 39h
    movd eax, xmm2
    mov [rbx + 28], eax
    shufps xmm2, xmm2, 39h
    movd eax, xmm2
    mov [rbx + 16], eax
    shufps xmm2, xmm2, 39h

    movd eax, xmm2
    mov [rbx + 4], eax

    ; save blue
    movd eax, xmm1
    mov [rbx +36], eax
    shufps xmm1, xmm1, 39h
    movd eax, xmm1
    mov [rbx + 24], eax
    shufps xmm1, xmm1, 39h
    movd eax, xmm1
    mov [rbx + 12], eax
    shufps xmm1, xmm1,39h

    movd eax, xmm1
    mov [rbx], eax


	pop rbx
	ret
Calculate endp


END