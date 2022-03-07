use64
org 0x140001000
function_140001000:                     
	sub	rsp, 40
	mov	ecx, 3
	call 0x140001070
	lea	ecx, [rax + 10]
	test	eax, eax
	mov	eax, 4294967295
	cmovne	rax, rcx
	add	rsp, 40
	ret
