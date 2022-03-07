source_filename = "test"
target datalayout = "e-m:e-p:64:64-i64:64-f80:128-n8:16:32:64-S128"

define i64 @function_140001000() local_unnamed_addr {
dec_label_pc_140001000:
  %0 = call i64 @function_140001070(i64 3), !insn.addr !0
  %1 = trunc i64 %0 to i32, !insn.addr !1
  %2 = add i64 %0, 10
  %3 = icmp eq i32 %1, 0, !insn.addr !2
  %4 = icmp eq i1 %3, false, !insn.addr !3
  %phitmp = and i64 %2, 4294967295
  %storemerge1 = select i1 %4, i64 %phitmp, i64 4294967295
  ret i64 %storemerge1, !insn.addr !4
}

declare i64 @function_140001070(i64) local_unnamed_addr

!0 = !{i64 5368713225}
!1 = !{i64 5368713230}
!2 = !{i64 5368713280}
!3 = !{i64 5368713285}
!4 = !{i64 5368713316}
